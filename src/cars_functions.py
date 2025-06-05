import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache_data
def read_df_cars():
    file_path = '../data/electric_vehicles/bestand_cars.csv'
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
    fig = px.bar(df, x=df.index, y="e_cars", color_discrete_sequence=['red'])
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
    fig = px.line(df, x=df.index, y="%e_cars", color_discrete_sequence=['blue'], markers=True)
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