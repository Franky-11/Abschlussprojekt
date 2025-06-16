from tkinter.messagebox import showerror

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import json

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


@st.cache_data
def read_df_cars_for_map():
    df=pd.read_csv("data/Anteil_BEV.csv")
    df['schluessel'] = df['schluessel'].astype(str).str.zfill(2)
    return df


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


# Bestandsdiagrammme für TAB1
@st.cache_data
def read_df_fuel():
    df = pd.read_csv("data/Bestand_PKW_nach Kraftstoffarten.csv", delimiter=";")
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
                 showarrow=True, arrowhead=2, ax=-120, ay=-100, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="gray",
                 borderwidth=1, borderpad=4),
            dict(x='2023', y=0.6, yref='paper', text="Umweltbonus endet für Firmenkunden", showarrow=True,
                 arrowhead=2, ax=-180, ay=-60, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="gray", borderwidth=1,
                 borderpad=4),
            dict(x='2024', y=0.8, yref='paper', text="Umweltbonus endet abrupt!", showarrow=True, arrowhead=2,
                 ax=0, ay=-80, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="red", borderwidth=2, borderpad=4,
                 font=dict(color="red", weight="bold")),
            # dict(x='2023-01-01', y=0.05, yref='paper', text="Plug-in-Hybride nicht mehr gefördert", showarrow=True,
            # arrowhead=2, ax=0, ay=40, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="gray", borderwidth=1,
            # borderpad=4),
            dict(x='2021', y=0.2, yref='paper', text="EU-CO2-Flottenziele verschärft<br>(Herstellerdruck)",
                 showarrow=True, arrowhead=2, ax=0, ay=-100, bgcolor="rgba(255, 255, 255, 0.8)", bordercolor="gray",
                 borderwidth=1, borderpad=4)
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

