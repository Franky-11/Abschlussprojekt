import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.optimize import minimize

from cars_functions import read_geojson_landkreise



def run():
    @st.cache_data
    def read_df_lade_bev():
        df = pd.read_csv("data/df_lade_bev.csv")
        df["Kreis_code"] = df["Kreis_code"].astype(str).str.zfill(5)
        df = df.drop_duplicates(subset="Kreis_code", keep="first")
        df["pkw_ratio"] = df["Bestand_PKW"] / df["Bestand_PKW"].sum()
        df["lp_ratio"] = df["Anzahl_Ladepunkte_0425"] / df["Anzahl_Ladepunkte_0425"].sum()
        return df

    # ------------------- Optimierungsfunktionen -------------------

    def zielfunktion(lp, bev, ziel):
        return np.sum((bev / lp - ziel) ** 2)

    def kostenfunktion(lp, bev, ziel, gewicht):
        fehler = np.sum((bev / lp - ziel)**2)
        kosten = np.sum(lp)
        return fehler + gewicht * kosten

    def ladepunkt_summe(lp, zielsumme):
        return np.sum(lp) - zielsumme

    # ------------------- Kartenfunktion -------------------

    def plot_map(df, geojson_kreise, column, label,range_column):
        min_val = df[range_column].min()
        max_val = df[range_column].max()

        fig = px.choropleth_mapbox(
            df,
            geojson=geojson_kreise,
            locations="Kreis_code",
            featureidkey="properties.RS",
            color=column,
            color_continuous_scale="Reds",
            range_color=[min_val, max_val],
            mapbox_style="carto-positron",
            zoom=5,
            center={"lat": 51.0, "lon": 10.0},
            opacity=0.8,
            hover_name="Landkreis_y",
            hover_data={column:":.1f"}
        )

        fig.update_layout(
            margin={"r":0,"t":0,"l":0,"b":0},
            coloraxis_colorbar={"title": f"∅ BEV / LP ({label})"}
        )
        fig.update_traces(marker_line_width=0, marker_line_color='rgba(0,0,0,0)')

        return fig


    def info():
        st.markdown("""
                            **Verteilung der neuen BEV-Fahrzeuge:**  
                            Die prognostizierte Gesamtanzahl der Batterie-elektrischen Fahrzeuge (BEV) wird proportional zum aktuellen PKW-Bestand auf die einzelnen Landkreise verteilt.
                            $$ BEV_{Landkreis} = BEV_{Gesamt} \\times \\frac{PKW_{Landkreis}}{PKW_{Gesamt}} $$

                            **Lineare Verteilung der Ladepunkte:**  
                            Die anfängliche, "lineare" Verteilung der Ladepunkte erfolgt proportional zum aktuellen Bestand an Ladepunkten in den Landkreisen. Das heißt, Landkreise mit vielen Ladepunkten erhalten auch im prognostizierten Szenario mehr neue Ladepunkte.
                            $$ LP_{linear, Landkreis} = LP_{Gesamt} \\times \\frac{LP_{aktuell, Landkreis}}{LP_{aktuell, Gesamt}} $$

                            **Optimierungsziel (Modus "Fixe Ladepunktanzahl"):**  
                            In diesem Modus wird die Verteilung der Ladepunkte so optimiert, dass das Verhältnis von BEV pro Ladepunkt ($BEV/LP$) in allen Landkreisen möglichst nahe an einem definierten **Zielverhältnis** (z.B. 12 BEV pro Ladepunkt) liegt. Die Gesamtzahl der Ladepunkte bleibt dabei konstant ($LP_{gesamt}$).
                            Die Zielfunktion minimiert die Summe der quadrierten Abweichungen:
                            $$ \\min \\sum_{i=1}^{n} \\left( \\frac{BEV_i}{LP_i} - Ziel \\right)^2 $$
                            Unter der Nebenbedingung:
                            $$ \\sum_{i=1}^{n} LP_i = LP_{Gesamt} $$
                            Hierbei ist $BEV_i$ die Anzahl der BEV im Landkreis $i$, $LP_i$ die Anzahl der Ladepunkte im Landkreis $i$ und $Ziel$ das angestrebte BEV/LP-Verhältnis.

                            **Optimierungsziel (Modus "Kostenfunktion (frei)"):**  
                            Dieser Modus erlaubt eine flexiblere Verteilung, indem er nicht nur die Abweichung vom Zielverhältnis, sondern auch die Gesamtzahl der benötigten Ladepunkte berücksichtigt. Die Optimierung minimiert eine gewichtete Summe aus Fehlerquadraten und Gesamtkosten der Ladepunkte. Das Gewicht $$  \\beta $$ steuert, wie stark die Reduzierung der Ladepunkte bevorzugt wird, auch wenn dies zu größeren Abweichungen vom Zielverhältnis führt.
                            $$ \\min \\left( \\sum_{i=1}^{n} \\left( \\frac{BEV_i}{LP_i} - Ziel \\right)^2 \\right) + \\beta \\times \\left( \\sum_{i=1}^{n} LP_i \\right) $$
                            Hierbei ist $$  \\beta $$ das "Gewicht auf LP-Kosten" (Beta).

                            **Randbedingungen für Ladepunkte ($LP_i$):**  
                            Die Anzahl der Ladepunkte in einem Landkreis ($LP_i$) muss immer mindestens dem aktuellen Bestand ($LP_{aktuell, Landkreis}$) entsprechen und darf maximal so hoch sein, dass das BEV/LP-Verhältnis nicht unter 2 fällt ($LP_i \\le BEV_i / 2$), um eine sinnvolle Auslastung zu gewährleisten.
                            """)


    # ------------------- Streamlit App -------------------


    if "ansicht_links" not in st.session_state:
        st.session_state.ansicht_links = "IST"

    if "opt_erfolgreich" not in st.session_state:
        st.session_state.opt_erfolgreich = False

    if "lp_opt" not in st.session_state:
        st.session_state.lp_opt = None

    if "prognose" not in st.session_state:
        st.session_state.prognose = False

    if "ist" not in st.session_state:
        st.session_state.ist = True


    st.header("⚡ Ladeinfrastruktur-Prognose & Verteilung")

   # ansicht = st.radio(
    #    "🗺️ Auswahl Karte (links)",
   #     options=["IST", "LINEAR"],
   #     index=["IST", "LINEAR"].index(st.session_state.ansicht_links),
   #     horizontal=True
  #  )

   # st.session_state.ansicht_links = ansicht



    df = read_df_lade_bev()
    geojson_kreise = read_geojson_landkreise()

    # Container mit Seitenaufbau
    with st.container(border=True,height=1000):
        with st.popover("📚 Berechnungsgrundlagen", use_container_width=True):
            info()
        col_1, col_2 = st.columns(2)

        with col_1:
            col_pop,col_info,col_leer=st.columns([2,2,1])
            with col_pop:
                with st.popover("🔋 Prognose-Einstellungen"):
                    with st.form("prognose_form"):
                        bev_gesamt = st.slider("BEV-Prognose gesamt (Mio.)", 5.0, 52.0, 15.0, step=0.5) * 1_000_000
                        lp_gesamt = st.slider("Ladepunkt-Prognose gesamt", 170000,1000000, 400000, step=10000)
                        ist=st.checkbox("IST-Zustand",value=True)
                        submit = st.form_submit_button("📌 Karte aktualisieren")

        # BEV + LP-Prognose vorbereiten
        df["BEV_prog"] = df["pkw_ratio"] * bev_gesamt
        df["lp_prog_linear"] = df["lp_ratio"] * lp_gesamt
        df["BEV_prog_lp_prog_linear"] = df["BEV_prog"] / df["lp_prog_linear"]


        if submit:
            st.session_state.prognose = True
            st.session_state.ist = ist
            st.session_state.opt_erfolgreich = False
            st.session_state.lp_opt = None



        # ----------------------------------------------- Kartenbereich LINKS
        with col_1:
            if st.session_state.ist:
                st.session_state.ansicht_links = "IST"
                st.metric("∅ BEV / LP (IST)", value=f"{df['BEV_pro_Ladepunkt'].mean():.0f} ± {df['BEV_pro_Ladepunkt'].std():.0f}")
                fig_left = plot_map(df, geojson_kreise, "BEV_pro_Ladepunkt", "IST", "BEV_pro_Ladepunkt")
            else:
                delta=(df['BEV_prog_lp_prog_linear'].mean()-df['BEV_pro_Ladepunkt'].mean())/df['BEV_pro_Ladepunkt'].mean()*100
                st.metric("∅ BEV / LP (linear)", value=f"{df['BEV_prog_lp_prog_linear'].mean():.0f} ± {df['BEV_prog_lp_prog_linear'].std():.0f}",delta=f"{delta:.1f}% zum IST-Zustand",delta_color="inverse")
                fig_left = plot_map(df, geojson_kreise, "BEV_prog_lp_prog_linear", "linear", "BEV_prog_lp_prog_linear")
                st.session_state.ansicht_links = "LINEAR"


            st.plotly_chart(fig_left, use_container_width=True)



        # ------------------------- Optimierungsformular -------------------------
        with col_info:
            place_holder = st.empty()
            if st.session_state.prognose and not st.session_state.ist and not st.session_state.opt_erfolgreich:
                place_holder.info("Szenario noch nicht optimiert!")

        with col_2:
            if not st.session_state.ist:
                with st.popover("🔧 Ladepunkt-Optimierung"):

                    with st.form("opt_form"):
                        st.markdown(f"""
                                    🔢 **Ausgewählte Parameter**:  
                                        {bev_gesamt / 1e6:.1f} Mio. BEV  
                                        {lp_gesamt} Ladepunkte""")
                        st.divider()
                        ziel_ratio = st.slider("🎯 Zielverhältnis BEV / Ladepunkt", 5.0, 50.0, 12.0)
                        opt_modus = st.selectbox("Optimierungsmodus", ["Fixe Ladepunktanzahl", "Kostenfunktion (frei)"])

                        #gewicht = None
                        #if opt_modus == "Kostenfunktion (frei)":
                        gewicht = st.number_input("⚖️ Gewicht auf LP-Kosten (Beta)", 0.0, 0.1, 0.0,step=0.01,help="Wenn Modus Kostenfunktion ausgewählt: Beta steuert, wie stark zusätzliche Ladepunkte 'kosten'. Höhere Werte bevorzugen sparsame Verteilungen – auch wenn das Zielverhältnis dann schlechter getroffen wird.")

                        start_opt = st.form_submit_button("🚀 Optimierung starten")

                        if start_opt:
                            with st.spinner("⏳ Optimierung läuft..."):
                                bev = df["BEV_prog"].values
                                min_lp = df["Anzahl_Ladepunkte_0425"].values  # Untere Grenze LP Verteilung
                                x0 = df["lp_prog_linear"].values   # Start Verteilung ladepunkte
                                #bounds = [(min_, None) for min_ in min_lp]
                                bounds = [
                                    (min_, bev_i / 2)  #  Maximal erlaubte Ladepunkte, sodass BEV/LP ≥ 2
                                    for min_, bev_i in zip(min_lp, bev)]

                                if opt_modus == "Fixe Ladepunktanzahl":
                                    constraint = {"type": "eq", "fun": lambda lp: ladepunkt_summe(lp, lp_gesamt)}
                                    res = minimize(
                                        zielfunktion,
                                        x0,
                                        args=(bev, ziel_ratio),
                                        method="SLSQP",
                                        bounds=bounds,
                                        constraints=[constraint]
                                    )
                                else:
                                    res = minimize(
                                        kostenfunktion,
                                        x0,
                                        args=(bev, ziel_ratio, gewicht),
                                        method="SLSQP",
                                        bounds=bounds
                                    )

                                st.session_state.lp_opt = res.x
                                st.session_state.opt_erfolgreich = True
                                st.session_state.prognose=False

                                st.success("✅ Optimierung abgeschlossen!")
                                place_holder.write("")



    # ------------------------- Ergebnisse anzeigen -------------------------

    if st.session_state.opt_erfolgreich and st.session_state.lp_opt is not None:
        df["lp_opt"] = st.session_state.lp_opt
        df["BEV_prog_lp_opt"] = df["BEV_prog"] / df["lp_opt"]
        df["LP_diff"] = df["lp_opt"] - df["Anzahl_Ladepunkte_0425"]

        with col_2:
            col_met,col_param,col_check=st.columns([1,1,1])
            with col_met:
                delta_opt=(df['BEV_prog_lp_opt'].mean()-df['BEV_prog_lp_prog_linear'].mean())/df['BEV_prog_lp_prog_linear'].mean()*100
                st.metric("∅ BEV / LP (optimiert)", value=f"{df['BEV_prog_lp_opt'].mean():.0f} ± {df['BEV_prog_lp_opt'].std():.0f}",delta=f"{delta_opt:.1f}% zur linearen LP-Skalierung",delta_color="inverse")
            with col_param:
                st.markdown(
                    f"""
                    **🔢 Parameterübersicht**  
                    {bev_gesamt / 1e6:.1f} Mio. BEV  
                    {df['lp_opt'].sum() / 1e6:.3f} Mio. Ladepunkte
                    """
                )

            with col_check:
                check=st.checkbox("Ansicht zusätzliche Ladepunkte")
            if not check:
                fig_right = plot_map(df, geojson_kreise, "BEV_prog_lp_opt", "optimiert", "BEV_prog_lp_prog_linear")
            else:
                fig_right = plot_map(df, geojson_kreise, "LP_diff", "Zusätzliche Ladepunkte", "LP_diff")

            st.plotly_chart(fig_right, use_container_width=True)

            if check:
                df_opt = df[["Landkreis_y", "BEV_prog_lp_opt", "lp_opt", "LP_diff"]]
                df_opt.columns = ["Landkreis", "BEV/Lp optimiert", "Lp optimiert", "Zusätzlich benötigte Lp"]
                df_opt_sorted = df_opt.sort_values(by="Zusätzlich benötigte Lp", ascending=False).round(0)
                with st.popover("Ladepunkte nach Optimierung", use_container_width=True):
                    st.dataframe(df_opt_sorted)




#st.set_page_config(layout="wide")
#run()