import streamlit as st

from strombedarf_functions import *

def run():

    col1,col2=st.columns([1,1])
    with col1:
        st.header("")
        st.write("")

        st.title("Strombedarf:material/electric_bolt:")

    with col2:
        st.image("images/electricity-2595842_1280.jpg",use_container_width=True)


    st.divider()


    #--------------Frank Stromverbrauch BEV-----------"

    col1,col2=st.columns([4,2])


    with col1:
        tab1, tab2,tab3,tab4 = st.tabs([":material/battery_low: Stromverbrauch BEV", ":material/query_stats: Vergleich Quantile",":material/gesture_select: Vergleich Modelle",":material/distance: ∅ Reichweite"])
        with tab1:
            with st.container(border=True, height=500):
                df_verbrauch=read_verbrauchsdaten()
                desc_stats = df_verbrauch.groupby(["Segment", "Testart"])[
                    "Verbrauch_(kWh/100km)"].describe().reset_index().sort_values(by=["Segment","mean"])
                with st.popover("Deskriptive Statistik",use_container_width=True):
                    st.dataframe(desc_stats.round(1),hide_index=True,use_container_width=True)
                fig=plot_verbrauch(df_verbrauch)
                st.plotly_chart(fig)
                with st.popover("Quellen anzeigen"):
                    st.markdown("""
                            * Verbauchsdaten: ADAC, TCS (Touring Club Schweiz), ÖAMTC (Österreichischer Automobil-, Motorrad- und Touring Club) 
                            * Reichweite BEV: ADAC
                            Was ist WLTP:  
                            WLTP steht für **Worldwide Harmonized Light-Duty Vehicles Test Procedure** (Weltweit harmonisiertes Prüfverfahren für leichte Nutzfahrzeuge).  
                            """)


        with tab2:
            with st.container(border=True,height=500):
                fig=plot_quantile(df_verbrauch)
                st.plotly_chart(fig)

        with tab3:
            with st.container(border=True,height=650):
                with st.popover("Segmente auswählen"):
                    with st.form("Modellauswahl"):
                        check_col1,check_col2=st.columns(2)
                        with check_col1:
                            mini=st.checkbox("Minis & Kleinwagen")
                            kompakt=st.checkbox("Kompaktklasse")
                            mittel=st.checkbox("Mittelklasse")
                            obere=st.checkbox("Obere Mittelklasse & Oberklasse")
                        with check_col2:
                            suv=st.checkbox("SUVs & Geländewagen")
                            uti=st.checkbox("Utilities, Mini-Vans & Großraum-Vans")
                            sonst=st.checkbox("Sonstige")

                        seg = df_verbrauch["Segment"].unique().tolist()
                        check_list = [mini, kompakt, mittel, obere, suv, uti, sonst]
                        seg_filtered = segments(check_list, seg)
                        df_filtered_seg = segment_filter(df_verbrauch, seg_filtered)
                        modelle = sorted(df_filtered_seg["Modell"].unique().tolist())
                        st.form_submit_button("Segmente auswählen")

                selected_modell = st.multiselect("Modelle", options=modelle, default=modelle[0:3])
                df_modell_filtered=modell_filter(df_filtered_seg,selected_modell)

                if df_modell_filtered.empty:
                    selected_modell = ["Renault Twingo Z.E.","Tesla Model 3 Long Range AWD","Mercedes EQV 300"]
                    fig=plot_modell_verbrauch(df_verbrauch[(df_verbrauch["Modell"].isin(selected_modell)) & (df_verbrauch["Testart"]=="Realer Verbrauch")])
                else:
                    df_modell_filtered = modell_filter(df_filtered_seg, selected_modell)
                    fig = plot_modell_verbrauch(df_modell_filtered)
                st.plotly_chart(fig)
        with tab4:
            with st.container(border=True,height=500):
                df_reichweite=read_reichweite()
                fig=plot_reichweite(df_reichweite)
                st.plotly_chart(fig)




    stats = df_verbrauch.groupby("Testart")["Verbrauch_(kWh/100km)"].describe().reset_index()
    delta=(stats.loc[0,"mean"]-stats.loc[1,"mean"])/stats.loc[1,"mean"]*100
    mini=stats.loc[0,"min"]
    maxi=stats.loc[0,"max"]

    max_reichweite=df_reichweite["Durchschnittliche Reichweite (km)"].max()
    min_reichweite=df_reichweite["Durchschnittliche Reichweite (km)"].min()
    delta_reichweite=(max_reichweite-min_reichweite)/min_reichweite*100

    with col2:
        st.markdown(":material/monitoring: **Key facts**")

        st.metric(label="Mittlerer Verbrauch BEV",value=f"{stats.loc[0,"mean"]:.1f} kWh/100km",delta=f"{delta:.1f}% zum WLTP",delta_color="inverse")

        st.write("")

        st.metric(label=" ∅ Reichweite BEV", value=f"{max_reichweite} km",
                  delta=f"{delta_reichweite:.0f}% zu 2014", delta_color="normal")



        #st.markdown("------------------------------------------")

    if "strombedarf_szenarien" not in st.session_state:
        st.session_state.strombedarf_szenarien = {2025:None,2030:None,2035:None}



    st.divider()

    def strombedarf_szenarien(fahrzeuge, verbrauch, jahres_km):
        return fahrzeuge * verbrauch * (jahres_km / 100)


    st.title("🔌 Strombedarf-Simulator")
    st.markdown("Berechnung des BEV-Strombedarfs für verschiedene Szenarien")

    st.sidebar.header("📊 Eingaben")
    szenario = st.sidebar.radio("Szenario", ["2025", "2030", "2035"])
    fahrzeuge = st.sidebar.slider("Fahrzeuganzahl (in Mio.)", 1, 52, 2) * 1_000_000
    verbrauch = st.sidebar.slider("Verbrauch (kWh / 100 km)", 10, 25, 20)
    jahres_km = st.sidebar.slider("Jahresfahrleistung (km)", 8000, 20000, 12000)
    lastmanagement = st.sidebar.checkbox("Lastmanagement aktivieren")

    # Slider-Eingaben statt feste Szenario-Werte verwenden
    strombedarf = strombedarf_szenarien(fahrzeuge, verbrauch, jahres_km)
    strombedarf_twh = strombedarf / 1e9

    st.metric("🔋 Strombedarf gesamt", f"{strombedarf_twh:.2f} TWh für {szenario}")

    df = pd.DataFrame({
        "Szenario": [szenario],
        "Fahrzeuge": [fahrzeuge],
        "Verbrauch (kWh/km)": [verbrauch],
        "Jahres-km": [jahres_km],
        "Lastmanagement": [lastmanagement],
        "Strombedarf (TWh)": [strombedarf_twh]
    })

    st.download_button("📥 Ergebnisse als CSV herunterladen", df.to_csv(index=False),
                       file_name="strombedarf_szenario.csv", mime="text/csv")

    # --- Plotly Stacked Bar Chart: Strombedarf vs. EE ---
    jahre = list(range(2025, 2036))
   # bev_bedarf = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]
    ee_erzeugung = [12.139*jahr-24280 for jahr in jahre]          ## Gesamt Stromerzeugung aus erneuerbaren energien, Prognose nach UBA Daten
    ee={jahr:tw for jahr,tw in zip(jahre,ee_erzeugung)}

   # rest_ee = [ee - bev for ee, bev in zip(ee_erzeugung, bev_bedarf)]



    # Aktuellen Nutzerwert im Szenariojahr einfügen
  #  jahr_index = jahre.index(int(szenario))
   # bev_bedarf[jahr_index] = strombedarf_twh
   # rest_ee[jahr_index] = max(0, ee_erzeugung[jahr_index] - strombedarf_twh)

    jahr = int(szenario)
    strombedarf = strombedarf_szenarien(fahrzeuge, verbrauch, jahres_km)
    strombedarf_twh = strombedarf / 1e9

    # Session-State aktualisieren
    st.session_state.strombedarf_szenarien[jahr] = strombedarf_twh

    #jahre = list(range(2025, 2036))
   # bev_bedarf = [st.session_state.strombedarf_szenarien.get(j, 0) for j in jahre]
    #rest_ee = [max(0, ee - bedarf) for ee, bedarf in zip(ee_erzeugung, bev_bedarf)]

    jahre_szen, bedarf_szen = zip(*[
        (jahr, val) for jahr, val in st.session_state.strombedarf_szenarien.items() if val is not None ])

    rest_ee = [ee[jahr]-bedarf for jahr,bedarf in zip(jahre_szen,bedarf_szen)]
    bev_prozent=[(bedarf/ee[jahr])*100 for jahr,bedarf in zip(jahre_szen,bedarf_szen)]

    def plot_fig(check):
        fig = go.Figure()
        if not check:
            fig.add_trace(go.Bar(
                name="🔋 BEV-Strombedarf",
                x=jahre_szen,
                #y=bev_bedarf,
                y=bedarf_szen,
                text=[f"{y:.1f} TWh" for y in bedarf_szen],
                textfont=dict(size=18),
                marker_color="#636EFA"))

            fig.add_trace(go.Bar(
                name="🌿 Gesamterzeugung aus EE",
               # x=jahre,
                x=jahre_szen,
                #y=rest_ee,
                y=rest_ee,
                marker_color="#00CC96"))

            fig.update_layout(
                barmode='stack',
               # title="⚡ Strombedarf der E-Mobilität vs. EE-Erzeugung (2025–2035)",
               # xaxis_title="Jahr",
                yaxis_title="Energie (TWh)",
                template="plotly_white",
                legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center", yanchor="bottom"),
                height=500)
        else:
            fig.add_trace(go.Bar(
                name="🔋 Anteil BEV-Strombedarf",
                x=jahre_szen,
                # y=bev_bedarf,
                y=bev_prozent,
                text=[f"{y:.1f}%" for y in bev_prozent],
                textfont=dict(size=18),
                marker_color="#636EFA"))

            gewuenschte_jahre_ticks = [2025, 2030, 2035]

            fig.update_layout(
                barmode='stack',
                #title="⚡ Strombedarf der E-Mobilität vs. EE-Erzeugung (2025–2035)",
                #xaxis_title="Jahr",
                yaxis_title="Anteil Strombedarf BEV (%)",
                # Beachte, dass dein BEV-Anteil auf einer anderen Skala ist, was beim Stacken problematisch sein könnte.
                # Vielleicht willst du hier eine sekundäre Y-Achse für den Prozentanteil?
                template="plotly_white",
                legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center", yanchor="bottom"),
                height=500,
                xaxis=dict(
                    tickmode='array',  # Wichtig: Sagt Plotly, dass du die Ticks manuell setzt
                    tickvals=gewuenschte_jahre_ticks,  # Die Werte, an denen die Ticks erscheinen sollen
                    ticktext=[str(jahr) for jahr in gewuenschte_jahre_ticks]  # Die Beschriftungen für die Ticks
                )
            )



        return fig

    if "check" not in st.session_state:
        st.session_state.check=False



    with st.container(border=True, height=600):
        st.markdown("⚡ Strombedarf der E-Mobilität vs. Gesamterzeugung aus erneuerbaren Energien (EE)")
        st.session_state.check = st.checkbox("Anteil Strombedarf BEV an EE")
        fig=plot_fig(st.session_state.check)
        st.plotly_chart(fig, use_container_width=True)

#st.set_page_config(layout="wide")
#run()
