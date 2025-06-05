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
def plot_e_cars(df):
    fig = px.bar(df, x=df.index, y="e_cars", color_discrete_sequence=['red'])
    fig.update_xaxes(title_text="",range=['2018-06-01','2025-03-01'])
    fig.update_yaxes(title_text="Bestand E-Car",range=[0, 1.8*1E6])

    annotations = [
        # Innovationsprämie (Juli 2020)
        dict(
            x='2020-07-01',  # Datum auf der X-Achse
            y=0.3, yref='paper',  # y-Position (0=unten, 1=oben im Plotbereich)
            text="Innovationsprämie startet<br>(Verdopplung Umweltbonus)",  # Text der Annotation
            showarrow=True,  # Pfeil anzeigen
            arrowhead=2,  # Art des Pfeilkopfs
            ax=0, ay=-100,  # Pfeilversatz (ax=x-Versatz, ay=y-Versatz)
            bgcolor="rgba(255, 255, 255, 0.8)",  # Hintergrundfarbe
            bordercolor="gray",  # Randfarbe
            borderwidth=1,  # Randbreite
            borderpad=4,  # Abstand zum Rand
            # font=dict(size=10, color="darkblue") # Schriftart
        )]

    fig.update_layout(annotations=annotations)

    return fig


@st.cache_data
def plot_e_cars_percent(df):
    fig = px.line(df, x=df.index, y="%e_cars", color_discrete_sequence=['blue'], markers=True)
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="E-Car Anteil (%)")
    return fig