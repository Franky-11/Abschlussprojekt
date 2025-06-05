import streamlit as st
import pandas as pd



@st.cache_data
def lade_und_bereinige_daten(pfad):
    df = pd.read_csv(pfad,
                     sep=';',
                     encoding='ISO-8859-1',
                     dtype=str)
    relevante_spalten = ["Breitengrad", "Längengrad", "Ort", "Straße", "Hausnummer", "Art der Ladeeinrichtung"]

    # Fehlende Werte entfernen
    df = df[relevante_spalten].dropna(subset=["Breitengrad", "Längengrad"])

    def ist_gueltig(val):
        val = str(val).replace('.', '')
        return val.isdigit()

    def format_breitengrad(val):
        val = str(val).replace('.', '')
        val = val.ljust(8, '0')[:8]
        return f"{val[:-6]}.{val[-6:]}"  # z.B. 51805270 → 51.805270

    def format_laengengrad(val):
        val = str(val).replace('.', '')
        if val.startswith("1"):
            val = val.ljust(8, '0')[:8]
        else:
            val = val.ljust(7, '0')[:7]
        return f"{val[:-6]}.{val[-6:]}"  # z.B. 10332870 → 10.332870

    df = df[df["Breitengrad"].apply(ist_gueltig)]
    df = df[df["Längengrad"].apply(ist_gueltig)]

    df["Breitengrad"] = df["Breitengrad"].apply(format_breitengrad).astype(float)
    df["Längengrad"] = df["Längengrad"].apply(format_laengengrad).astype(float)

    # Nur Koordinaten in Deutschland behalten
    df = df[
        df["Breitengrad"].between(47.0, 55.1) &
        df["Längengrad"].between(5.5, 15.5)
        ]

    return df

