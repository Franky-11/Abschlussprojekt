
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.optimize import curve_fit
from sklearn.metrics import r2_score,root_mean_squared_error
import plotly.graph_objects as go
import json

"""
# Alte Visualisierung

@st.cache_data
def read_df_cars():
    file_path = 'data/bestand_cars.csv'
    df = pd.read_csv(file_path, delimiter=";")
    df["date"] = pd.to_datetime(df["date"], format='%d.%m.%Y')
    df.set_index(df["date"], inplace=True)
    df.drop("date", axis=1, inplace=True)
    df["cars_sum"] = df["cars_sum"].str.replace(".", "")
    df["cars_sum"] = pd.to_numeric(df["cars_sum"])
    df["e_cars"] = df["e_cars"].str.replace(".", "")
    df["e_cars"] = pd.to_numeric(df["e_cars"])
    df["%e_cars"] = (df["e_cars"] / df["cars_sum"]) * 100

    return df

@st.cache_data
def plot_cars(df):
    fig = px.bar(df, x=df.index, y="cars_sum")
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Bestand PKW")
    fig.update_yaxes(range=[45 * 1E6, 50 * 1E6])
    return fig

@st.cache_data
def plot_e_cars(df,annot):
    #fig = px.bar(df, x=df.index, y="e_cars", color_discrete_sequence=['red'])
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["e_cars"],
        fill="tozeroy",
        fillcolor='rgba(255,0,0,0.2)',
        line_color='rgba(255,0,0,1)',
        showlegend=False,
        name='e_cars',
    ))
    fig.update_xaxes(title_text="",range=['2018-06-01','2025-03-01'])
    fig.update_yaxes(title_text="Bestand E-Car",range=[0, 1.8*1E6])

    if annot:
        annotations = [
            dict(x='2020-07-01', y=0.1, yref='paper', text="Innovationsprämie startet<br>(Verdopplung Umweltbonus)",
                 showarrow=True, arrowhead=2, ax=-120, ay=-100, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="gray",
                 borderwidth=1, borderpad=4),
            dict(x='2023-09-01', y=0.7, yref='paper', text="Umweltbonus endet für Firmenkunden", showarrow=True,
                 arrowhead=2, ax=-180, ay=-60, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="gray", borderwidth=1,
                 borderpad=4),
            dict(x='2023-12-18', y=0.8, yref='paper', text="Umweltbonus endet abrupt!", showarrow=True, arrowhead=2,
                 ax=0, ay=-80, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="red", borderwidth=2, borderpad=4,
                 font=dict(color="red", weight="bold")),
            #dict(x='2023-01-01', y=0.05, yref='paper', text="Plug-in-Hybride nicht mehr gefördert", showarrow=True,
                # arrowhead=2, ax=0, ay=40, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="gray", borderwidth=1,
                 #borderpad=4),
            dict(x='2021-01-01', y=0.2, yref='paper', text="EU-CO2-Flottenziele verschärft<br>(Herstellerdruck)",
                 showarrow=True, arrowhead=2, ax=0, ay=-100, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="gray",
                 borderwidth=1, borderpad=4)
        ]
        fig.update_layout(annotations=annotations)


    return fig


@st.cache_data
def plot_e_cars_percent(df,annot=False):
    #fig = px.line(df, x=df.index, y="%e_cars", color_discrete_sequence=['blue'], markers=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df.index,
        y=df["%e_cars"],
        fill="tozeroy",
        fillcolor='rgba(0,0,255,0.2)',
        line_color='rgba(0,0,255,1)',
        showlegend=False,
        name='e_cars',
    ))

    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="E-Car Anteil (%)")

    if annot:
        annotations = [
            dict(x='2020-07-01', y=0.1, yref='paper', text="Innovationsprämie startet<br>(Verdopplung Umweltbonus)",
                 showarrow=True, arrowhead=2, ax=-120, ay=-100, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="gray",
                 borderwidth=1, borderpad=4),
            dict(x='2023-09-01', y=0.7, yref='paper', text="Umweltbonus endet für Firmenkunden", showarrow=True,
                 arrowhead=2, ax=-180, ay=-60, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="gray", borderwidth=1,
                 borderpad=4),
            dict(x='2023-12-18', y=0.8, yref='paper', text="Umweltbonus endet abrupt!", showarrow=True, arrowhead=2,
                 ax=0, ay=-80, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="red", borderwidth=2, borderpad=4,
                 font=dict(color="red", weight="bold")),
            # dict(x='2023-01-01', y=0.05, yref='paper', text="Plug-in-Hybride nicht mehr gefördert", showarrow=True,
            # arrowhead=2, ax=0, ay=40, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="gray", borderwidth=1,
            # borderpad=4),
            dict(x='2021-01-01', y=0.2, yref='paper', text="EU-CO2-Flottenziele verschärft<br>(Herstellerdruck)",
                 showarrow=True, arrowhead=2, ax=0, ay=-100, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="gray",
                 borderwidth=1, borderpad=4)
        ]
        fig.update_layout(annotations=annotations)

    return fig

"""

#-----------------------------------------------------------------------------#
#Bundeslandkarte mit Verteilung BEV

@st.cache_data
def read_df_cars_for_map():
    df=pd.read_csv("data/Anteil_BEV.csv")
    df['schluessel'] = df['schluessel'].astype(str).str.zfill(2)
    return df

""""
@st.cache_data
def read_geojson():
    with open('data/bundeslaender_wgs84.geojson', 'r', encoding='utf-8') as f:
        geojson_bundeslaender_wgs84 = json.load(f)

    return geojson_bundeslaender_wgs84


@st.cache_data
def plot_car_map(df_cars_for_map,geojson):
    fig = px.choropleth_map(df_cars_for_map,
                            geojson=geojson,  # Die konvertierte GeoJSON-Datei
                            locations="schluessel",  # Spalte im DataFrame, die den 2-stelligen Schlüssel enthält
                            featureidkey="properties.schluessel",  # Pfad zum 'schluessel' im GeoJSON-Feature
                            color="BEV_pro_1000_Einwohner",  # Spalte, die die Farbe der Region bestimmt
                            color_continuous_scale="Blues",
                            # Farbskala (z.B. "Viridis", "Plasma", "Jet", "Greens", "Blues")
                            range_color=(
                            df_cars_for_map["BEV_pro_1000_Einwohner"].min(), df_cars_for_map["BEV_pro_1000_Einwohner"].max()),
                            # mapbox_style="carto-positron",     # Basiskarte (z.B. "open-street-map", "carto-positron", "stamen-terrain")
                            zoom=5,  # Zoom-Level für Deutschland (ca. 4.5 - 5.5)
                            center={"lat": 51.0, "lon": 10.0},  # Zentraler Punkt für Deutschland
                            opacity=0.8,  # Deckkraft der eingefärbten Regionen
                            hover_name="Bundesland",  # Was im Tooltip als Haupttitel angezeigt wird
                            hover_data={'BEV_pro_1000_Einwohner': ':.0f', 'schluessel': False, "Anteil_BEV": ':.2f',
                                        "PKW_Gesamt": ":,.0f"},
                            height=700
                            )
    return fig


"""

#-------Fahrzeugbestand nach Kraftstoffarten und Entwicklung BEV-Bestand / Neuzulassungen-------------------------------------------------------------------------------------#



@st.cache_data
def read_df_fuel():
    df = pd.read_csv("data/Bestand_PKW_nach_Kraftstoffarten.CSV", delimiter=";")
    value_vars = ['Benzin', 'Diesel', 'Gas', "BEV", 'Hybrid', "Sonstige"]
    id_vars = ['Jahr']
    df_long = pd.melt(df,
                      id_vars=id_vars,
                      value_vars=value_vars,
                      var_name='Kraftstoff',
                      value_name='Wert')

    return df_long

def layout():
    settings = {
        "hovermode": "x unified",
        "uniformtext_minsize": 16,
        # Font-Größen
        "yaxis_title_font_size": 16,
        "legend_font_size": 16,
        "xaxis_tickfont_size": 16,
        "yaxis_tickfont_size": 16,
        # Grid entfernen
        "xaxis": {"showgrid": False},  # Hier muss xaxis auch ein dict sein
        "yaxis": {"showgrid": False}  # Hier muss yaxis auch ein dict sein
    }
    return settings




@st.cache_data
def plot_car_fuel(df_long):
    fig = px.area(df_long, x="Jahr", y="Wert", color="Kraftstoff", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="PKW Bestand nach Kraftstoffarten")
    fig.update_layout(**layout())

    fig.update_traces(hovertemplate="<b>%{fullData.name}</b><br>" +  # Name der Kennzahl (z.B. Benzin, Diesel)
                                    "%{y:,.0f}<extra></extra>" )


    return fig

@st.cache_data
def plot_bev(df_long,annot):
    fig = px.area(df_long[df_long["Kraftstoff"] == "BEV"], x="Jahr", y="Wert", color="Kraftstoff",
                  color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="PKW Bestand nach Kraftstoffarten")
    fig.update_layout(**layout())
    fig.update_traces(hovertemplate="<b>%{fullData.name}</b><br>" +  # Name der Kennzahl (z.B. Benzin, Diesel)
                                    "%{y:,.0f}<extra></extra>"
                      # Wert mit Tausender-Trennzeichen und ohne Dezimalstellen
                      )

    if annot:
        annotations = [
            dict(x='2020', y=0.1, yref='paper', text="Innovationsprämie startet<br>(Verdopplung Umweltbonus)",
                 showarrow=True, arrowhead=2, ax=-120, ay=-100, bgcolor="rgba(50, 50, 50, 0.8)", bordercolor="gray",
                 borderwidth=1, borderpad=4,font=dict(color="white")),
            dict(x='2023', y=0.6, yref='paper', text="Umweltbonus endet für Firmenkunden", showarrow=True,
                 arrowhead=2, ax=-180, ay=-60, bgcolor="rgba(50, 50, 50, 0.8)", bordercolor="gray", borderwidth=1,
                 borderpad=4,font=dict(color="white")),
            dict(x='2024', y=0.8, yref='paper', text="Umweltbonus endet abrupt!", showarrow=True, arrowhead=2,
                 ax=0, ay=-80, bgcolor="rgba(50, 50, 50, 0.8)", bordercolor="red", borderwidth=2, borderpad=4,
                 font=dict(color="red", weight="bold")),
            # dict(x='2023-01-01', y=0.05, yref='paper', text="Plug-in-Hybride nicht mehr gefördert", showarrow=True,
            # arrowhead=2, ax=0, ay=40, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="gray", borderwidth=1,
            # borderpad=4),
            dict(x='2021', y=0.2, yref='paper', text="EU-CO2-Flottenziele verschärft<br>(Herstellerdruck)",
                 showarrow=True, arrowhead=2, ax=0, ay=-100, bgcolor="rgba(50, 50, 50, 0.8)", bordercolor="gray",
                 borderwidth=1, borderpad=4,font=dict(color="white"))
        ]

        fig.update_layout(annotations=annotations)

    return fig


@st.cache_data
def read_df_neu_bev():
    """
    liest neuzulassung bev ein, entwicklung der neuzulassungen der bev über die jahre
    :return: DataFrame mit Neuzulassungen
    """
    df_neuzu_bev=pd.read_csv("data/neuzulassung_bev.csv",delimiter=";",encoding='latin-1')
    return df_neuzu_bev


@st.cache_data
def plot_neu_bev(df_neuzu_bev):
    """
    Erstellt plot Entwicklung der Neuzulassungen BEV
    :param df_neuzu_bev:
    :return: fig
    """
    fig = px.area(df_neuzu_bev, x="jahr", y="BEV", color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Neuzulassungen BEV")
    fig.update_layout(**layout())
    fig.update_traces(hovertemplate="<b>%{fullData.name}</b><br>" +  # Name der Kennzahl (z.B. Benzin, Diesel)
                                    "%{y:,.0f}<extra></extra>" )
    return fig



#------- Verteilung BEV auf PLZ Ebene---------------------------------------------------------------------------#

"""

@st.cache_data
def read_geojson_plz():
    with open('data/georef-germany-postleitzahl.geojson', 'r', encoding='utf-8') as f:
        geojson_plz = json.load(f)
    return geojson_plz


@st.cache_data
def read_df_geo():

    data = {"PLZ": [], "lon": [], "lat": [], "plz_name_long": [], "krs_name": [], "krs_code": []}
    geojson_plz=read_geojson_plz()

    for kreis in geojson_plz["features"]:
        data["PLZ"].append(kreis["properties"]["plz_code"])
        data["plz_name_long"].append(kreis["properties"]["plz_name_long"])
        data["krs_name"].append(kreis["properties"]["krs_name"])
        data["krs_code"].append(kreis["properties"]["krs_code"])
        data["lon"].append(kreis["properties"]["geo_point_2d"]["lon"])
        data["lat"].append(kreis["properties"]["geo_point_2d"]["lat"])

    df_geo = pd.DataFrame(data)

    return df_geo


@st.cache_data
def read_df_cars_for_plz_map():
    df_geo=read_df_geo()
    df_bev_plz = pd.read_csv("data/BEV_nach_plz.csv", delimiter=";", encoding='latin-1')
    df_bev_plz["PLZ"] = df_bev_plz["PLZ"].astype(str).str.zfill(5)
    df_bev_plz["Anteil_BEV"] = df_bev_plz["Bestand_BEV"] / df_bev_plz["Bestand_PKW"] * 100
    bev_kreise = pd.merge(df_bev_plz, df_geo, how="left", on="PLZ")
    bev_kreise.dropna(inplace=True)

    return bev_kreise


#@st.cache_data
def plot_car_plz_map(bev_kreise,zoom_level,center_map,geojson_plz):
    fig = px.choropleth_map(bev_kreise,
                            geojson=geojson_plz,  # Die konvertierte GeoJSON-Datei
                            locations="PLZ",  # Spalte im DataFrame, die den 2-stelligen Schlüssel enthält
                            featureidkey="properties.plz_code",  # Pfad zum 'schluessel' im GeoJSON-Feature
                            # (wie in Ihrer GeoJSON-Struktur gesehen: 'properties': {'schluessel': '06', ...})
                            color="Anteil_BEV",  # Spalte, die die Farbe der Region bestimmt
                            color_continuous_scale="Blues",
                            # Farbskala (z.B. "Viridis", "Plasma", "Jet", "Greens", "Blues")
                            range_color=[0, 5],  # Stellen Sie sicher, dass die Farbskala die volle Bandbreite abdeckt
                            map_style="carto-positron",
                            # Basiskarte (z.B. "open-street-map", "carto-positron", "stamen-terrain")
                            zoom=zoom_level,  # Zoom-Level für Deutschland (ca. 4.5 - 5.5)
                            center=center_map,  # Zentraler Punkt für Deutschland
                            opacity=0.8,  # Deckkraft der eingefärbten Regionen
                            hover_name="plz_name_long",  # Was im Tooltip als Haupttitel angezeigt wird
                            hover_data={'Anteil_BEV': ':.1f', "Bestand_PKW": ":,.0f", 'PLZ': False,
                                        "Bestand_BEV": ":,.0f"},
                            # Optional: Formatiert die Anzeige der PKW_Bestand im Tooltip (als ganze Zahl)
                            # title="PKW-Bestand pro Bundesland in Deutschland" # Titel der Karte
                            )

    fig.update_traces(marker_line_width=0, marker_line_color='rgba(0,0,0,0)')

    return fig

"""

#----------BEV auf Kreisebene--------------------------------#

@st.cache_data
def read_geojson_landkreise():
    with open("data/landkreise_simplify200.geojson", 'r', encoding='utf-8') as f:
        geojson_kreise = json.load(f)

    return geojson_kreise




@st.cache_data
def read_df_kreise_land():
    df=pd.read_csv("data/df_kreise_land.CSV")
    df["Kreis_code"] = df["Kreis_code"].astype(str).str.zfill(5)
    df["SN_L"] = df["SN_L"].astype(str).str.zfill(2)
    return df


def info_bundesland(df_filtered):
    info = df_filtered[["Bundesland", "Bestand_PKW_Bundesland", "Bestand_BEV_Bundesland", "Anteil_BEV_Bundesland"]]
    info = info.drop_duplicates(subset="Bundesland")
    return info



def plot_bev_kreise(df_filtered,geojson_kreise):
    hover_data = hover_data = {
        "Bundesland": True,
        "Anteil_BEV": ':.1f',
        "Anteil_BEV_Bundesland": ':.1f',
        "Delta_Anteil_BEV_Kreis_vs_Bundesland%": ':.1f',
        "Bestand_PKW": ":,.0f",
        "Bestand_BEV": ":,.0f",
        "Kreis_code": False
    }

    fig = px.choropleth_map(df_filtered,
                            geojson=geojson_kreise,  # Die konvertierte GeoJSON-Datei
                            locations="Kreis_code",  # Spalte im DataFrame, die den 2-stelligen Schlüssel enthält
                            featureidkey="properties.RS",  # Pfad zum 'schluessel' im GeoJSON-Feature
                            # (wie in Ihrer GeoJSON-Struktur gesehen: 'properties': {'schluessel': '06', ...})
                            color="Anteil_BEV",  # Spalte, die die Farbe der Region bestimmt
                            color_continuous_scale="Blues",
                            # Farbskala (z.B. "Viridis", "Plasma", "Jet", "Greens", "Blues")
                            range_color=[0, 5],  # Stellen Sie sicher, dass die Farbskala die volle Bandbreite abdeckt
                            map_style="carto-positron",
                            # Basiskarte (z.B. "open-street-map", "carto-positron", "stamen-terrain")
                            zoom=5,  # Zoom-Level für Deutschland (ca. 4.5 - 5.5)
                            center={"lat": 51.0, "lon": 10.0},  # Zentraler Punkt für Deutschland
                            opacity=0.8,  # Deckkraft der eingefärbten Regionen
                            hover_name="Landkreis",  # Was im Tooltip als Haupttitel angezeigt wird
                            hover_data=hover_data
                            # {'Anteil_BEV': ':.1f','Anteil_BEV_Bundesland': ':.1f','Delta_Anteil_BEV_Kreis_vs_Bundesland%': ':.1f',"Bestand_PKW":":,.0f",'Kreis_code': False,"Bestand_BEV":":,.0f"}, # Optional: Formatiert die Anzeige der PKW_Bestand im Tooltip (als ganze Zahl)
                            # title="PKW-Bestand pro Bundesland in Deutschland" # Titel der Karte
                            )

    fig.update_traces(marker_line_width=0, marker_line_color='rgba(0,0,0,0)')
    return fig










#-------- BEV nach Segmenten-------------------------------------------------------------------------------------------------#
# Diagramm 1
@st.cache_data
def read_df_bev_segmente(long=True):
    df = pd.read_csv("data/bestand_nach_segment.csv", delimiter=";", encoding='latin-1')
    df["PKW_ohne_BEV"] = df["PKW_Gesamt"] - df["BEV"]
    sum_bev_2024 = df[df["Jahr"] == 2024]["BEV"].sum()
    sum_bev_2023 = df[df["Jahr"] == 2023]["BEV"].sum()
    sum_pkw_2024 = df[df["Jahr"] == 2024]["PKW_ohne_BEV"].sum()
    sum_pkw_2023 = df[df["Jahr"] == 2023]["PKW_ohne_BEV"].sum()

    def anteil_segment(row):
        if row["Jahr"] == 2024:
            return (row["BEV"] / sum_bev_2024) * 100
        elif row["Jahr"] == 2023:
            return (row["BEV"] / sum_bev_2023) * 100

    def anteil_segment_pkw(row):
        if row["Jahr"] == 2024:
            return (row["PKW_ohne_BEV"] / sum_pkw_2024) * 100
        elif row["Jahr"] == 2023:
            return (row["PKW_ohne_BEV"] / sum_pkw_2023) * 100

    df["Anteil_Segment_BEV"] = df.apply(anteil_segment, axis=1)

    df["Anteil_Segment_PKW"] = df.apply(anteil_segment_pkw, axis=1)

    df["Penetration"] = (df["BEV"] / df["PKW_Gesamt"]) * 100

    df_sorted = df[df["Jahr"] == 2024].sort_values(by="Penetration", ascending=False)

    if long:
        id_vars = ["Jahr", "Segment"]
        value_vars = ["Anteil_Segment_BEV", "Anteil_Segment_PKW"]

        df_long = pd.melt(df, id_vars=id_vars,
                          value_vars=value_vars,
                          var_name='Anteil_Segment',
                          value_name='Wert')
        return df_long

    return df_sorted


@st.cache_data
def plot_bev_segmente(df_long):
    pull_segement = "SUVs"
    pull_values = [0.1 if pull_segement == segment else 0 for segment in df_long["Segment"]]

    fig = px.pie(df_long[df_long["Jahr"] == 2024], names="Segment", values="Wert", color="Segment",
                 color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.2, facet_col="Anteil_Segment",
                 category_orders={"Anteil_Segment": ["Anteil_Segment_PKW", "Anteil_Segment_BEV"]})
    fig.update_layout(uniformtext_minsize=14, uniformtext_mode='hide', showlegend=False, annotations=[
        dict(text="PKW ohne BEV", x=0.22, y=1.0, showarrow=False, font=dict(size=16)),
        dict(text="BEV", x=0.78, y=1.0, showarrow=False, font=dict(size=16))])

    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_traces(
        # hovertemplate zum Anpassen des Hover-Textes
        hovertemplate="<b>Segment: %{label}</b><br>" +
                      "Anteil: %{percent}<extra></extra>")

    fig.update_traces(pull=pull_values)
    return fig



#-- Diagramm 2 Anteil  BEV an  Neuzulassungen  nach Segmenten und Gesamt------------#

@st.cache_data
def read_df_bev_zulassung_segmente():
    df=pd.read_csv("data/bev_zulasssung_segmente.csv",delimiter=";",encoding='latin-1')
    df.drop("Unnamed: 4", axis=1, inplace=True)
    df.dropna(inplace=True)

    df["Segment"] = [" ".join(text.split()[0:2]) if text == "OBERE MITTELKLASSE ZUSAMMEN" else text.split()[0] for text
                     in df["Segment"]]

    df_sorted = df.sort_values(by=["Segment", "Jahr"]).reset_index(drop=True)
    df_sorted["penetration"] = (df_sorted["Anzahl_BEV"] / df_sorted["Gesamt"]) * 100

    df_gesamt = df_sorted.groupby("Jahr").agg({"Gesamt": ["sum"], "Anzahl_BEV": ["sum"]}).reset_index()
    df_gesamt["Anteil_BEV_Gesamt"] = df_gesamt[("Anzahl_BEV", "sum")] / df_gesamt[("Gesamt", "sum")] * 100
    df_gesamt["Segment"] = "Gesamt"
    df_gesamt["gesamt_pkw"] = df_gesamt[("Gesamt", "sum")]
    df_gesamt["gesamt_BEV"] = df_gesamt[("Anzahl_BEV", "sum")]
    df_for_concat = df_gesamt[["Jahr", "Segment", "gesamt_pkw", "gesamt_BEV", "Anteil_BEV_Gesamt"]]
    df_for_concat = df_for_concat.droplevel(1, axis=1)
    df_for_concat.columns = df_sorted.columns
    df_for_plot = pd.concat([df_sorted, df_for_concat], axis=0, ignore_index=True)


    return df_for_plot

@st.cache_data
def plot_bev_zulassung_segmente(df_sorted,segmente):
    order = ["SUVs", "MINIS", "KLEINWAGEN", "KOMPAKTKLASSE", "MITTELKLASSE", "GELÄNDEWAGEN", "OBERE MITTELKLASSE",
             "OBERKLASSE", "UTILITIES", "SONSTIGE", "MINI-VANS", "GROSSRAUM_VANS"]

    fig = px.line(df_sorted[df_sorted["Segment"].isin(segmente)], x="Jahr", y="penetration", color="Segment",
                  color_discrete_sequence=px.colors.qualitative.Pastel,
                  category_orders={"Segment": order}, custom_data=["Gesamt", "Anzahl_BEV", "penetration"])
    fig.update_traces(fill='tozeroy')
    fig.update_xaxes(title_text="")

    fig.update_yaxes(title_text="Anteil BEV an Neuzulassungen %")

    fig.update_layout(**layout())

    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>" +  # Name des Segments
                      "Anzahl BEV: %{customdata[1]:,.0f}<br>" +  # Anzahl_BEV
                      "PKW Gesamt: %{customdata[0]:,.0f}<br>" +
                      "Anteil BEV: %{customdata[2]:.1f}%<extra></extra>")

    return fig


# Diagramm---------- 3-- Durchdringung in den  BEV- Segmente

@st.cache_data
def plot_bev_penetration(df_sorted):
    fig = px.bar(df_sorted, x="Segment", y="Penetration", color="Segment",
                 color_discrete_sequence=px.colors.qualitative.Pastel, custom_data=["BEV", "PKW_Gesamt", "Penetration"])
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="Penetrationsrate pro Segement %")
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>" +  # Name des Segments
                      "Anzahl BEV: %{customdata[0]:,.0f}<br>" +  # Anzahl_BEV
                      "PKW Gesamt: %{customdata[1]:,.0f}<br>" +
                      "Penetration: %{customdata[2]:.1f}%<extra></extra>")
    fig.update_layout(**layout())
    fig.update_layout(showlegend=False)

    return fig

# ----------BEV Prognose-----------------------------------------------
@st.cache_data
def read_df_bev_prognose():
    df_studien=pd.read_csv("data/Prognose_BEV_Fahrzeuge.csv",delimiter=";",encoding="latin")
    df_studien["Prognose_BEV"] = df_studien["Prognose_BEV"].str.replace(",", ".")
    df_studien["Prognose_BEV"] = pd.to_numeric(df_studien["Prognose_BEV"])

    df_pivot = pd.pivot(df_studien, columns=["Szenario", "Quelle"], values="Prognose_BEV", index="Jahr")
    df_pivot.columns = [f"{col[0]} - {col[1]}" for col in df_pivot.columns]

    return df_pivot

@st.cache_data
def plot_prognose_bev(df_pivot):
    fig = px.imshow(df_pivot,text_auto=True, color_continuous_scale=px.colors.sequential.Viridis)  # Oder 'Plasma', 'Inferno', 'Blues', etc. )
    fig.update_layout(xaxis=dict(showticklabels=False))
    fig.update_traces(hovertemplate=
                      "<b>Jahr:</b> %{y}<br>" +
                      "<b>Quelle:</b> %{x}<br>" +
                      "<b>Prognose:</b> %{z:,.1f} Mio.<extra></extra>")


    fig.update_layout(**layout())
    fig.update_layout(hovermode="closest")
    fig.update_layout(coloraxis_showscale=False)
    fig.update_xaxes(title_text="Studie/Quelle")

    return fig




#Tab2

@st.cache_data
def data_for_fit():
    df = pd.read_csv("data/Prognose_BEV_Fahrzeuge_fit.csv", delimiter=";", encoding="latin")
    df["Anzahl_Prognose"] = df["Anzahl_Prognose"].str.replace(",", ".")
    df["Anzahl_Prognose"] = pd.to_numeric(df["Anzahl_Prognose"])

    years = df["Jahr"]
    x_data = years - 2020
    y_data = df["Anzahl_Prognose"]

    return years,x_data,y_data


#def logistic_function(x, L, k,x0,L_const=None):

  #  if L_const is not None:
  #      L = L_const
  #  return L / (1 + np.exp(-k * (x - x0)))


def logistic_function_full(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))

def logistic_function_L_fixed(x, k, x0, fixed_L_value):
    return fixed_L_value / (1 + np.exp(-k * (x - x0)))


def best_fit(fixed_L=None):
    _, x_data, y_data=data_for_fit()
    if fixed_L is None:
        initial_guesses=[40,0.5,20]
        params, covariance = curve_fit(logistic_function_full, x_data, y_data, p0=initial_guesses)
        L,k,x0= params
        return L,k,x0

    #else:  # L ist konstant, k, x0 optimieren
       # initial_guesses = [0.5, 20]
        #params, covariance = curve_fit(logistic_function_L_fixed, x_data, y_data, p0=initial_guesses, args=(fixed_L,))
       # k, x0 = params
       # return fixed_L, k, x0

    else:
        def wrapped_logistic(x, k, x0):
            return logistic_function_L_fixed(x, k, x0, fixed_L)

        initial_guesses = [0.5, 20]
        params, _ = curve_fit(wrapped_logistic, x_data, y_data, p0=initial_guesses)
        k, x0 = params
        return fixed_L, k, x0




def plot_data_and_fit(L,k,x0,fit):
    years, x_data, y_data=data_for_fit()
    x_for_plot = np.linspace(2020, 2060, 100)
    x_for_fit = x_for_plot - 2020
    fitted_curve = logistic_function_full(x_for_fit, L, k, x0)


    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=y_data, name='Historische Daten & Prognosen', mode='markers'))
    if fit:
        fig.add_trace(go.Line(x=x_for_plot, y=fitted_curve, name='Logistischer Fit', hovertemplate=None,
                              line=dict(dash='dash', color='red', width=1)))


    fig.update_layout(yaxis_title='BEV-Fahrzeuge in Mio.')
    fig.update_layout(**layout())

    fig.update_layout(
        legend=dict(
            x=0.8,
            y=0.5,
            xanchor='center',
            yanchor='top',
            bordercolor='gray',
            borderwidth=0.2 ))


    return fig


def show_paramater(L,k,x0):
    _,x_data,y_data=data_for_fit()
    r=r2_score(y_data, logistic_function_full(x_data, L, k,x0))
    rmse=root_mean_squared_error(y_data, logistic_function_full(x_data, L, k,x0))

    df=pd.DataFrame({"Sättigung (Mio. BEV)":L,"Wachstumsrate":k,"Wendepunkt (Jahr)":int(x0+2020),"R^2":r,"RMSE":rmse},index=["Logistischer Fit"])
    st.dataframe(df,use_container_width=True)


#----TCO---------------------#
def tco_info():


    data = {
        "Strompreis (€ Cent/kWh)": [60, 45, 35, 18],
        "Anteil günstigerer E-Autos (%)": [16, 22, 28, 36]
    }
    df_costs = pd.DataFrame(data)


    df_costs = df_costs.sort_values(by="Strompreis (€ Cent/kWh)", ascending=False)


    df_costs["Strompreis_label"] = (
    df_costs["Strompreis (€ Cent/kWh)"]
    .astype(int)
    .astype(str)+ " ct")

    fig = px.bar(
        df_costs,
        x="Strompreis_label",
        y="Anteil günstigerer E-Autos (%)",
        title="Anteil der Modellpaarungen mit günstigeren BEV",
        text="Anteil günstigerer E-Autos (%)")

    fig.update_traces(
        texttemplate="%{text:.0f}%",
        textposition="outside",marker_color=px.colors.qualitative.Pastel[0])

    fig.update_yaxes(range=[0, 60])

    fig.update_layout(
        xaxis_title="Strompreis (ct/kWh)",
        yaxis_title="Anteil Paarungen mit günstigeren BEV (%)",
        xaxis_type="category",
        margin=dict(t=50, b=50))

    fig.update_layout(**layout())

    return fig