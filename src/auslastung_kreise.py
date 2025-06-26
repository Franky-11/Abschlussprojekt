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

    min_val_safe = min(min_val, cutoff_low)
    max_val_safe = max(max_val, cutoff_mid)

    # Und jetzt die Relativwerte wie gewohnt:
    low_rel = (cutoff_low - min_val_safe) / (max_val_safe - min_val_safe)
    mid_rel = (cutoff_mid - min_val_safe) / (max_val_safe - min_val_safe)

    color_scale = [
        [0.0, "#3CB043"],
        [low_rel, "#3CB043"],
        [low_rel, "#FFD700"],
        [mid_rel, "#FFD700"],
        [mid_rel, "#D1001F"],
        [1.0, "#D1001F"] ]

    #color_scale = [
      #  [0.0, "#3CB043"],  # sattes grün (🟢)
      #  [0.25, "#A8E05F"],  # helles grün-gelb
    #    [0.5, "#FFD700"],  # sonnengelb (🟡)
     #   [0.75, "#FFA500"],  # orange
    #    [1.0, "#D1001F"]  # signalrot (🔴)
 #   ]

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
                            range_color=[min_val_safe, max_val_safe],

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

    fig.update_layout(
        coloraxis_colorbar=dict(
            title=dict(
                text="∅ Ladepunktauslastung (h)",
                font=dict(size=14)), ticksuffix=" h"))

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


def save_df_auslastung(auslastung_status,nl_time,sl_time,bev_anteil,high_cut,low_cut):
    df_save = auslastung_status.copy()
    df_save.loc[:, "nl_time"] = nl_time
    df_save.loc[:, "sl_time"] = sl_time
    df_save.loc[:, "Anteil_BEV_Ladebedarf"] = bev_anteil
    df_save.loc[:, "cut_off_high"] = high_cut
    df_save.loc[:, "cut_off_low"] = low_cut
    if "df" in st.session_state and isinstance(st.session_state.df, pd.DataFrame):
        if not st.session_state.df.empty:
            max_id = st.session_state.df["szenario"].max()
            szenario_id = int(max_id) + 1
        else:
            szenario_id = 1
    else:
        szenario_id = 1

    df_save.loc[:, "szenario"] = szenario_id




    return df_save

def concat_df(df_session_state,df_save):
    df_szenarien = pd.concat([df_save,df_session_state, ], ignore_index=True)
    return df_szenarien

def szenarien(df_szenarien):
    df_szenarien["szenario_label"] = (
            df_szenarien["szenario"].astype(str) + "<br>" +
            "nl: " + df_szenarien["nl_time"].astype(str) + " min<br>" +
            "sl: " + df_szenarien["sl_time"].astype(str) + " min<br>" +
            "BEV-Anteil: " + (df_szenarien["Anteil_BEV_Ladebedarf"] * 100).round(1).astype(str) + "%<br>" +
            "cut-off: " + df_szenarien["cut_off_low"].astype(str) + "–" + df_szenarien["cut_off_high"].astype(
        str) + " h"
    )

    df_szenarien["hover_label"] = (
            df_szenarien["Auslastung"] + " | " +
            df_szenarien["Anteil Kreise (%)"].round(1).astype(str) + " % | " +
            "∅ " + df_szenarien["Mittlere Auslastung (h)"].round(1).astype(str) + " h"
    )
    szenarien = df_szenarien.copy()
    return szenarien

def plot_szenarien(szenarien):
    color_map = {
        "🟢 niedrig": "#3CB043",
        "🟡 mittel": "#FFD700",
        "🔴 hoch": "#D1001F"
    }

    fig = px.pie(
        szenarien,
        names="Auslastung",
        values="Anteil Kreise (%)",
        facet_col="szenario_label",  # falls du die Szenarien schon angereichert hast
        color="Auslastung",  # steuert Farben nach Ampel
        color_discrete_map=color_map,
        hole=0.1,
        hover_name="hover_label", hover_data=[])

    return fig


#-------------------------------------------------------------------------------------------------------------------------------------#
if "df" not in st.session_state:
    st.session_state.df=None

st.set_page_config(layout="wide")
st.subheader("Auslastung Ladeinfrastruktur")

with st.container(border=True):

    df_lade_bev=read_df_lade_bev()
    geojson_kreise=read_geojson_landkreise()

    with st.form("Auslastungsparameter"):
        col1,col2,col3=st.columns([2,1,2])
        with col1:
            nl_time=st.slider("Ladezeit Normalladepunkt (min)",min_value=120,max_value=240,step=10)
            sl_time = st.slider("Ladezeit Schnellladepunkt (min) ", min_value=10, max_value=60, step=10)
            bev_anteil=st.slider("BEV-Anteil mit Ladebedarf (%)",min_value=10,max_value=100,step=10)
            bev_anteil=bev_anteil/100
        with col2:
            pass
        with col3:
            high_cut=st.slider("Grenzwert hohe Auslastung (h)",min_value=6,max_value=15,step=1)
            low_cut=st.slider("Grenzwert niedrige Auslastung (h)",min_value=3,max_value=6,step=1)

        st.form_submit_button("Auslastung berechnen")

        df_auslastung = add_time_auslast_status(df_lade_bev, nl_time, sl_time, bev_anteil, high_cut, low_cut)
        info=auslastung_status(df_auslastung,high_cut,low_cut)


    # Szenario speichern und löschen
    col_speichern, col_reset = st.columns([1, 1])


    with col_speichern:
        if st.button("➕ Szenario speichern"):
            df_save = save_df_auslastung(info, nl_time, sl_time, bev_anteil, high_cut, low_cut)
            st.session_state.df = concat_df(st.session_state.df, df_save)
            st.success("Szenario wurde gespeichert.")

    with col_reset:
        if st.button("🔁 Alle Szenarien löschen"):
            st.session_state.df = None
            st.warning("Szenarien wurden gelöscht.")


    with st.popover("Auslastung Daten",use_container_width=True):
        info=auslastung_status(df_auslastung,high_cut,low_cut)
        st.dataframe(info,use_container_width=True,hide_index=True)

    fig=plot_auslastung(df_auslastung,geojson_kreise,high_cut,low_cut)
    st.plotly_chart(fig)



#df_save=save_df_auslastung(info,nl_time,sl_time,bev_anteil,high_cut,low_cut)

#df_szenarien=concat_df(st.session_state.df,df_save)
#st.session_state.df=df_szenarien

#szenarien=szenarien(df_szenarien)

if st.session_state.df is not None:
    df_szenarien = st.session_state.df
    szenarien = szenarien(df_szenarien)
    fig = plot_szenarien(szenarien)
    st.plotly_chart(fig, use_container_width=True)








