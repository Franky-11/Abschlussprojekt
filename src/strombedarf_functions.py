import streamlit as st

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from cars_functions import layout



#----Tab1---#
@st.cache_data
def read_verbrauchsdaten():
   df_verbrauch=pd.read_csv("data/bev_verbrauch_komplett.csv")
   df_verbrauch.loc[df_verbrauch["Testart"] == "Unabhängiger Verbauchstest", "Testart"] = "Realer Verbrauch"

   return df_verbrauch



@st.cache_data
def plot_verbrauch(df_verbrauch):
    fig = px.box(
        df_verbrauch,
        x="Segment",
        y="Verbrauch_(kWh/100km)",
        color="Testart",
        color_discrete_sequence=px.colors.qualitative.Pastel,
        points=False  # Keine Einzelpunkte anzeigen
    )

    fig.update_layout(
        yaxis_title='Verbrauch (kWh)',yaxis=dict(range=[10, 32]))

    fig.update_layout(**layout())
    fig.update_layout(xaxis=dict(tickfont_size=12,title="",showticklabels=True))
    fig.update_layout(yaxis=dict(showgrid=True))

    # Tooltip beschränken
    fig.update_traces(
        hovertemplate="<b>Segment:</b> %{x}<br>"
                      "<b>Q1 (25%):</b> %{q1:.1f} kWh<br>"
                      "<b>Median:</b> %{median:.1f} kWh<br>"
                      "<b>Q3 (75%):</b> %{q3:.1f} kWh<br>"
                      "<extra></extra>"
    )
    return fig



#----Tab2---#
@st.cache_data
def plot_quantile(df_verbrauch):
    stats = df_verbrauch.groupby("Testart")["Verbrauch_(kWh/100km)"].describe().reset_index()
    verbrauchswerte = {
        "Q1 (25%)": stats.loc[0, "25%"],
        "Q1 (25%) WLTP": stats.loc[1, "25%"],
        "Median": stats.loc[0, "50%"],
        "Median WLTP": stats.loc[1, "50%"],
        "Q3 (75%)": stats.loc[0, "75%"],
        "Q3 (75%) WLTP": stats.loc[1, "75%"]
    }
    max_wert = stats.max().iloc[-1]

    c = px.colors.qualitative.Pastel
    farbe = {"Q1 (25%)": c[0], "Median": c[1], "Q3 (75%)": c[2], "Q1 (25%) WLTP": c[0], "Median WLTP": c[1],
             "Q3 (75%) WLTP": c[2]}

    fig = go.Figure()

    for name, verbrauch in verbrauchswerte.items():
        fig.add_trace(go.Bar(
            x=[name],
            y=[verbrauch],
            marker_color=farbe[name],
            text=[f"{verbrauch:.1f}"],
            textfont=dict(size=16),
            textposition='outside',
            hoverinfo='skip'
        ))

    # Hintergrund-Skala (Max-Wert Balken)
    fig.add_trace(go.Bar(
        x=list(verbrauchswerte.keys()),
        y=[max_wert] * 6,
        marker_color='rgba(230,230,230,0.3)',
        hoverinfo='skip',
        showlegend=False
    ))

    fig.update_layout(
        barmode='overlay',
        yaxis=dict(range=[0, max_wert], title='Verbrauch (kWh/100 km)'),
        height=400,
        plot_bgcolor='white', showlegend=False, title="Quantile der Testverbräuche (je n=70)"
    )

    fig.update_layout(**layout())

    return fig


#----Tab3---#

def segments(check_list,seg):
    seg_filtered = [s for index, s in enumerate(seg) if check_list[index] == True]
    return seg_filtered



def segment_filter(df_verbrauch,seg_filtered):
    df_filtered_seg = df_verbrauch[(df_verbrauch["Segment"].isin(seg_filtered)) & (df_verbrauch["Testart"].isin(["Realer Verbrauch"]))]
    return df_filtered_seg


def modell_filter(df_filtered_seg,modell):
    df_modell_filtered=df_filtered_seg[df_filtered_seg["Modell"].isin(modell)]
    return df_modell_filtered




def plot_modell_verbrauch(df_modell_filtered):

    df_modell_filtered.sort_values(by="Verbrauch_(kWh/100km)", inplace=True)
    fig = px.bar(df_modell_filtered, x="Modell", y="Verbrauch_(kWh/100km)", color="Segment")

    fig.update_layout(
        barmode='group',
        yaxis=dict(range=[0, 31], title='Verbrauch (kWh/100 km)'), xaxis=dict(title="")),

    fig.update_layout(**layout())

    return fig


def plot_dist(df_verbrauch):
    anzahl=df_verbrauch.groupby("Segment")["Modell"].size()
    fig = px.pie(df_verbrauch)


# tab 4
@st.cache_data
def read_reichweite():
    df_reichweite=pd.read_csv("data/reichweite_BEV.csv")
    return df_reichweite

@st.cache_data
def plot_reichweite(df_reichweite):
    fig = px.area(df_reichweite, x="Jahr", y="Durchschnittliche Reichweite (km)",
                  color_discrete_sequence=[px.colors.qualitative.Pastel[0]])
    fig.update_layout(**layout())
    fig.update_layout(xaxis=dict(title=""))
    return fig




