import streamlit as st
import pandas as pd
import plotly.express as px
import os

def run():
    st.title("⚡ Stromerzeugung in Deutschland (CSV-Daten)")
    st.markdown("Visualisierung der **realisierten Erzeugung** nach Energieform auf Basis der SMARD-CSV-Daten.")

    # Pfad zur CSV-Datei
    csv_path = "data/smard/Realisierte_Erzeugung_202506210000_202507020000_Stunde_1.csv"

    if not os.path.exists(csv_path):
        st.warning("⚠️ CSV-Datei zur realisierten Erzeugung nicht gefunden.")
        return

    try:
        df = pd.read_csv(csv_path, sep=";", encoding="utf-8")
        st.caption(f"✅ Geladene Spalten: {list(df.columns)}")

        # Automatische Datumsspalten-Erkennung
        datum_col = next((c for c in df.columns if "Datum" in c or "Zeit" in c), None)
        if datum_col is None:
            st.error("❌ Keine Spalte mit Datum/Zeitangabe gefunden.")
            return

        df[datum_col] = pd.to_datetime(df[datum_col], errors="coerce", dayfirst=True)

        # Energieformen zur Auswahl (alle Spalten außer Datum)
        energieformen = df.columns.drop(datum_col)
        energieform = st.selectbox("🔌 Energieform wählen", energieformen)

        # Liniendiagramm
        fig = px.line(df, x=datum_col, y=energieform,
                      title=f"Realisierte Stromerzeugung: {energieform}",
                      labels={datum_col: "Zeit", energieform: "Erzeugung (MW)"})

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Fehler beim Verarbeiten der CSV-Datei: {e}")
