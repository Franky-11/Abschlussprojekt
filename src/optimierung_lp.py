import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from scipy.optimize import minimize


from cars_functions import read_geojson_landkreise


@st.cache_data
def read_df_lade_bev():
    df = pd.read_csv("data/df_lade_bev.csv")
    df["Kreis_code"] = df["Kreis_code"].astype(str).str.zfill(5)
    df = df.drop_duplicates(subset="Kreis_code", keep="first")
    sum_pkw = df["Bestand_PKW"].sum()
    sum_lp = df["Anzahl_Ladepunkte_0425"].sum()
    df["pkw_ratio"] = df["Bestand_PKW"] / sum_pkw
    df["lp_ratio"] = df["Anzahl_Ladepunkte_0425"] / sum_lp
    return df




# Ziel: Fehlerquadrate minimieren
def zielfunktion(lp, bev, ziel):
    return np.sum((bev / lp - ziel) ** 2)

# Ziel mit Kostenfunktion (Fehler + Gewicht * Ladepunkte)
def kostenfunktion(lp, bev, ziel, gewicht):
    fehler = np.sum((bev / lp - ziel)**2)
    kosten = np.sum(lp)
    return fehler + gewicht * kosten

# Nebenbedingung (nur bei fixer Summe)
def ladepunkt_summe(lp):
    return np.sum(lp) - ladepunkt_gesamt


def plot_map(df,geojson_kreise,column="BEV_pro_Ladepunkt"):
    min_val = df["BEV_pro_Ladepunkt"].min()
    max_val = df["BEV_pro_Ladepunkt"].max()

    fig = px.choropleth_map(df,
                            geojson=geojson_kreise,
                            locations="Kreis_code",
                            featureidkey="properties.RS",
                            color=column,
                            # color_continuous_scale=color_scale,
                            range_color=[min_val, max_val],

                            # color="status",
                            # color_discrete_map={"hoch": "red", "mittel": "yellow","niedrig":"green"},
                            color_continuous_scale="Reds",
                            # range_color=[0,10], #
                            map_style="carto-positron",
                            zoom=5,
                            center={"lat": 51.0, "lon": 10.0},
                            opacity=0.8,
                            hover_name="Landkreis_y")
    # hover_data=hover_data)

    fig.update_layout(
        coloraxis_colorbar=dict(
            title=dict(
                text="column",
                font=dict(size=14))))

    fig.update_traces(marker_line_width=0, marker_line_color='rgba(0,0,0,0)')
    return fig




if "submit" not in st.session_state:
    st.session_state.submit = False




st.set_page_config(layout="wide")

st.header("⚡ Ladeinfrastruktur-Prognose und Optimierung")

df=read_df_lade_bev()

with st.container(border=True):
    col_1, col_2 = st.columns(2)
    # BEV-Parameter
    with col_1:
        with st.popover("BEV und Ladepunkt-Prognose"):
            with st.form("Fahrzeuge und Ladepunkte"):
                bev_gesamt = st.slider("🔋 BEV-Prognose gesamt (in Mio.)", 2.0, 20.0, 15.0, step=0.5) * 1_000_000
                ladepunkt_gesamt = st.number_input("🛠️ Ladepunkt-Prognose gesamt", value=166_000, step=10_000)
                st.session_state.submit=st.form_submit_button("Karte aktualisieren")

    geojson_kreise = read_geojson_landkreise()
    df["BEV_prog"] = df["pkw_ratio"] * bev_gesamt
    df["lp_prog_linear"] = df["lp_ratio"] * ladepunkt_gesamt
    df["BEV_prog_lp_prog_linear"] = df["BEV_prog"] / df["lp_prog_linear"]
    min_lp = df["Anzahl_Ladepunkte_0425"].values
    start_lp = df["Anzahl_Ladepunkte_0425"].values

    # Startwert & Schranken
    bounds = [(min_, None) for min_ in min_lp]  # nicht weniger lp als Status quo
    x0 = start_lp.copy()


    with col_2:
        with st.popover("Optimierung Ladepunktverteilung"):
            with st.form("Optimierung Ladepunktverteilung"):
                ziel_ratio = st.slider("🎯 Zielwert BEV je Ladepunkt", 5.0, 50.0, 12.0)
                optimierung_modus = st.selectbox(
                    "Optimierungsmodus",
                    ["Fixe Ladepunktanzahl (z. B. 400.000)", "Kostenfunktion (freie Ladepunktzahl)"])

                submit_opt = st.form_submit_button("🚀 Optimierung starten")



    if st.session_state.submit:
        fig = plot_map(df, geojson_kreise, column="BEV_prog_lp_prog_linear")  # plot der prog werte /lineare Ladepunktskalierung
        with col_1:
            st.metric("Prognose Wert BEV pro Ladepunkt, lineare Skalierung LP", value=f"{df['BEV_prog_lp_prog_linear'].mean():.1f}")
    else:
        fig = plot_map(df, geojson_kreise)  # ist zustand BEV_pro Ladepunkt
        with col_1:
            st.metric("IST-Wert BEV pro Ladepunkt", value=f"{df['BEV_pro_Ladepunkt'].mean():.1f}")


    with col_1:
        st.plotly_chart(fig, use_container_width=True)


    if submit_opt:
        bev = df["BEV_prog"].values

        if optimierung_modus == "Fixe Ladepunktanzahl (z. B. 400.000)":
            res = minimize(
                zielfunktion, x0, args=(bev, ziel_ratio),
                method="SLSQP",
                bounds=bounds,
                constraints={"type": "eq", "fun": ladepunkt_summe}
            )
        else:
            gewicht = st.slider("⚖️ Gewicht auf Ladepunktkosten (beta)", 0.0, 0.01, 0.001)
            res = minimize(
                kostenfunktion, x0, args=(bev, ziel_ratio, gewicht),
                method="SLSQP",
                bounds=bounds
            )

        df["lp_opt"] = res.x
        df["BEV_prog_lp_opt"] = df["BEV_prog"] / df["lp_opt"]
        df["LP_diff"] = df["lp_opt"] - df["Anzahl_Ladepunkte_0425"]
        st.success("Optimierung abgeschlossen!")


        with col_2:
            st.metric("Optimierter Wert-BEV pro Ladepunkt", value=f"{df['BEV_prog_lp_opt'].mean():.1f}")
            fig2 = plot_map(df, geojson_kreise, column="BEV_prog_lp_opt")
            st.plotly_chart(fig2, use_container_width=True)







"""

# User Inputs
bev_gesamt = st.slider("🔋 BEV-Prognose gesamt (in Mio.)", 2.0, 20.0, 15.0, step=0.5) * 1_000_000
ladepunkt_gesamt = st.number_input("🛠️ Ladepunkt-Prognose gesamt", value=400_000, step=10_000)
ziel_ratio = st.slider("🎯 Zielwert BEV je Ladepunkt", 5.0, 50.0, 12.0)

optimierung_modus = st.selectbox(
    "Optimierungsmodus",
    ["Fixe Ladepunktanzahl (z. B. 400.000)", "Kostenfunktion (freie Ladepunktzahl)"])



df=read_df_lade_bev()

# Daten vorbereiten
df["BEV_prog"] = df["pkw_ratio"] * bev_gesamt
min_lp = df["Anzahl_Ladepunkte_0425"].values
start_lp = df["Anzahl_Ladepunkte_0425"].values





# Startwert & Schranken
bounds = [(min_, None) for min_ in min_lp]  # nicht weniger als Status quo
x0 = start_lp.copy()


if st.button("🚀 Optimierung starten"):
    bev = df["BEV_prog"].values

    if optimierung_modus == "Fixe Ladepunktanzahl (z. B. 400.000)":
        res = minimize(
            zielfunktion, x0, args=(bev, ziel_ratio),
            method="SLSQP",
            bounds=bounds,
            constraints={"type": "eq", "fun": ladepunkt_summe}
        )
    else:
        gewicht = st.slider("⚖️ Gewicht auf Ladepunktkosten (beta)", 0.0, 0.01, 0.001)
        res = minimize(
            kostenfunktion, x0, args=(bev, ziel_ratio, gewicht),
            method="SLSQP",
            bounds=bounds
        )


    df["lp_opt"] = res.x
    df["BEV_prog_lp_opt"] = df["BEV_prog"] / df["lp_opt"]
    df["LP_diff"] = df["lp_opt"] - df["Anzahl_Ladepunkte_0425"]
    st.success("Optimierung abgeschlossen!")


    min_val = df["BEV_prog_lp_opt"].min()
    max_val = df["BEV_prog_lp_opt"].max()

    geojson_kreise=read_geojson_landkreise()


    fig = px.choropleth_mapbox(
        df, geojson=geojson_kreise,
        locations="Kreis_code", featureidkey="properties.RS",
        color="BEV_prog_lp_opt",
        range_color=[min_val, max_val],
        mapbox_style="carto-positron",
        color_continuous_scale="Reds",
        center={"lat": 51.0, "lon": 10.0}, zoom=5,
        opacity=0.8,
        hover_name="Landkreis_y",
        hover_data={"BEV_prog_lp_opt":":.1f", "lp_opt":":.0f"}
    )
    fig.update_layout(
        margin={"r":0,"t":0,"l":0,"b":0},
        coloraxis_colorbar={"title":"∅ BEV/LP (optimiert)"}
    )
    st.plotly_chart(fig, use_container_width=True)

"""