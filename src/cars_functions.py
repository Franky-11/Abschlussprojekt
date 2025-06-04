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
def plot_e_cars(df,percent):
    if not percent:
        fig = px.bar(df, x=df.index, y="e_cars", color_discrete_sequence=['red'])
        fig.update_xaxes(title_text="")
        fig.update_yaxes(title_text="Bestand E-Car")
        return fig
    else:
        fig = px.line(df, x=df.index, y="%e_cars", color_discrete_sequence=['blue'], markers=True)
        fig.update_xaxes(title_text="")
        fig.update_yaxes(title_text="E-Car Anteil (%)")
        return fig