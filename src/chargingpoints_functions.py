import streamlit as st
import pandas as pd
import numpy as np

@st.cache_data
def load_data():
    df = pd.read_csv(
        "C:/Users/PC/Desktop/Abschlussprojekt/data/electric_vehicles/Ladesaeulenregister_BNetzA.csv",
        encoding="latin1",
        delimiter=";",
        parse_dates=["Inbetriebnahmedatum"],
        dayfirst=True
    )
    # Halbjährliche Kategorisierung
    months = df["Inbetriebnahmedatum"].dt.month
    df["Halbjahr"] = (
        df["Inbetriebnahmedatum"].dt.year.astype(str)
        + "-H"
        + np.where(months <= 6, "1", "2")
    )
    return df



@st.cache_data
def berechne_entwicklung(spalte, df):
    df_k = df.dropna(subset=["Inbetriebnahmedatum"]).copy()
    df_k["Wert"] = df_k[spalte].astype(float)
    ser = df_k.groupby("Halbjahr")["Wert"].sum().sort_index()
    df_kum = ser.cumsum().reset_index()
    df_kum.columns = ["Halbjahr", "Kumuliert"]
    return df_kum

@st.cache_data
def berechne_entwicklung_nach_art(df):
    df_k = df.dropna(subset=["Inbetriebnahmedatum", "Art der Ladeeinrichtung"]).copy()
    df_k["Wert"] = df_k["Anzahl Ladepunkte"].astype(float)
    df_group = df_k.groupby(["Halbjahr", "Art der Ladeeinrichtung"])["Wert"].sum().unstack(fill_value=0).sort_index()
    return df_group

@st.cache_data
def prognose_linear_referenz(df_kum, von_halbjahr="2022-H2", bis_halbjahr="2023-H2", ziel_halbjahr="2030-H2"):
    start = df_kum[df_kum["Halbjahr"] == von_halbjahr]["Kumuliert"].values[0]
    end = df_kum[df_kum["Halbjahr"] == bis_halbjahr]["Kumuliert"].values[0]
    delta = end - start
    step = delta / 2

    letzter = df_kum["Kumuliert"].iloc[-1]
    jahr, hz = map(int, df_kum["Halbjahr"].iloc[-1].split("-H"))
    halbjahre, werte = [], []
    while f"{jahr}-H{hz}" < ziel_halbjahr:
        if hz == 1:
            hz = 2
        else:
            hz = 1
            jahr += 1
        letzter += step
        halbjahre.append(f"{jahr}-H{hz}")
        werte.append(letzter)
    return pd.DataFrame({"Halbjahr": halbjahre, "Kumuliert": werte})