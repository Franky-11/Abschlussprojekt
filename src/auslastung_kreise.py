import streamlit as st
import pandas as pd
import plotly.express as px

from cars_functions import read_geojson_landkreise

@st.cache_data
def read_df_lade_bev():
    df = pd.read_csv("data/df_lade_bev.csv")
    df["Kreis_code"] = df["Kreis_code"].astype(str).str.zfill(5)
    df["NL_ratio"] = (df["NL"] / df["Anzahl_Ladepunkte_0425"])
    df["SL_ratio"] = (df["SL"] / df["Anzahl_Ladepunkte_0425"])
    return df


def add_time_auslast_status(df,nl_time,sl_time,bev_anteil,high_cut,low_cut):
    df["mean_charg_time_(min)"] = (df["SL_ratio"] * sl_time) + (df["NL_ratio"] * nl_time)
    df["auslastung_(h)"]=((df["mean_charg_time_(min)"])/60)*(df["Bestand_BEV"]*bev_anteil)/df["Anzahl_Ladepunkte_0425"]

    def status(row, high_cut, low_cut):
        if row["auslastung_(h)"] >high_cut:
            return "🔴 hoch"
        elif row["auslastung_(h)"] >low_cut:
            return "🟡 mittel"
        else:
            return "🟢 niedrig"

    df["status"] = df.apply(lambda row: status(row, high_cut, low_cut), axis=1)

    return df


def plot_auslastung(df,geojson_kreise,high_cut,low_cut):
    min_val = df["auslastung_(h)"].min()
    max_val = df["auslastung_(h)"].max()
    cutoff_low = low_cut
    cutoff_mid = high_cut

    max_val_safe = max(max_val, cutoff_mid)

    # Relative Positionen der Schwellenwerte in der Skala (0…1)
    low_rel = (cutoff_low - min_val) / (max_val_safe - min_val)
    mid_rel = (cutoff_mid - min_val) / (max_val_safe - min_val)

    color_scale = [
        [0.0, "#3CB043"],
        [low_rel, "#3CB043"],
        [low_rel, "#FFD700"],
        [mid_rel, "#FFD700"],
        [mid_rel, "#D1001F"],
        [1.0, "#D1001F"]
    ]

    hover_data = {
        "auslastung_(h)": ":.1f",
        "status": True,
        "Kreis_code": False,
        "Landkreis_y": False  # optional, wenn schon in hover_name
    }
    fig = px.choropleth_map(df,
                            geojson=geojson_kreise,
                            locations="Kreis_code",
                            featureidkey="properties.RS",
                            color="auslastung_(h)",
                            color_continuous_scale=color_scale,
                            range_color=[min_val, max_val_safe],

                            # color="status",
                            # color_discrete_map={"hoch": "red", "mittel": "yellow","niedrig":"green"},
                            # color_continuous_scale="Reds",
                            # range_color=[0,10], #
                            map_style="carto-positron",
                            zoom=5,
                            center={"lat": 51.0, "lon": 10.0},
                            opacity=0.8,
                            hover_name="Landkreis_y",
                            hover_data=hover_data)

    fig.update_traces(marker_line_width=0, marker_line_color='rgba(0,0,0,0)')

    return fig


def auslastung_status(df_auslastung,high_cut,low_cut):
    status_kreise = (df_auslastung["status"].value_counts(normalize=True) * 100).round(1).reset_index()
    auslastung = df_auslastung.groupby("status")["auslastung_(h)"].agg(
        Mittel="mean",
        Std="std"
    ).reset_index().round(1)
    auslastung_status = pd.merge(status_kreise, auslastung, on="status")

    def cutoff(x):
        if x == "🔴 hoch":
            return f">{high_cut} h"
        elif x == "🟡 mittel":
            return f"{low_cut}-{high_cut} h"
        else:
            return f"<{low_cut} h"

    auslastung_status["cut_off"] = auslastung_status["status"].apply(cutoff)
    auslastung_status.columns = ["Auslastung", "Anteil Kreise (%)", "Mittlere Auslastung (h)", "Std (h)",
                                 "Gewählter cut_off"]
    neue_reihenfolge = ["Auslastung", "Gewählter cut_off", "Anteil Kreise (%)", "Mittlere Auslastung (h)", "Std (h)"]
    auslastung_status = auslastung_status[neue_reihenfolge]
    return auslastung_status


#----------------------------------------------------------------------------

st.subheader("Auslastung Ladeinfrastruktur")

with st.container(border=True):

    df_lade_bev=read_df_lade_bev()
    geojson_kreise=read_geojson_landkreise()

    with st.form("Auslastungsparameter"):
        col1,col2=st.columns(2)
        with col1:
            nl_time=st.slider("Ladezeit Normalladepunkt (min)",min_value=120,max_value=240,step=10)
            sl_time = st.slider("Ladezeit Schnellladepunkt (min) ", min_value=30, max_value=60, step=10)
            bev_anteil=st.slider("BEV-Anteil mit Ladebedarf (%)",min_value=10,max_value=100,step=10)
            bev_anteil=bev_anteil/100
        with col2:
            high_cut=st.slider("Grenzwert hohe Auslastung (h)",min_value=6,max_value=15,step=1)
            low_cut=st.slider("Grenzwert niedrige Auslastung (h)",min_value=3,max_value=6,step=1)
        st.form_submit_button("Auslastung berechnen")

    df_auslastung = add_time_auslast_status(df_lade_bev, nl_time, sl_time, bev_anteil, high_cut, low_cut)



    with st.popover("Auslastung Daten",use_container_width=True):
        info=auslastung_status(df_auslastung,high_cut,low_cut)
        st.dataframe(info,use_container_width=True,hide_index=True)

    fig=plot_auslastung(df_auslastung,geojson_kreise,high_cut,low_cut)
    st.plotly_chart(fig)










