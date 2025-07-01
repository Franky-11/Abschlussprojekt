import streamlit as st
import pandas as pd
import plotly.express as px
import os

def run():
    st.title("📊 Installierte Erzeugungsleistung")
    st.markdown("Wähle eine Energieform zur Visualisierung der installierten Leistung (MW).")

    # Lokale CSV-Datei laden
    file_path = "data/smard/Installierte_Erzeugungsleistung_202506210000_202507020000_Stunde_2.csv"

    if not os.path.exists(file_path):
        st.error(f"❌ Datei nicht gefunden: `{file_path}`")
        return

    try:
        df = pd.read_csv(file_path, sep=";", encoding="utf-8")
        st.caption(f"📁 Geladene Spalten: {list(df.columns)}")

        # Datum-Spalte identifizieren (auch wenn sie anders heißt)
        datum_spalte = next((col for col in df.columns if "Datum" in col or "Zeit" in col), None)
        if datum_spalte is None:
            st.error("❌ Keine Spalte gefunden, die 'Datum' oder 'Zeit' enthält.")
            return

        df[datum_spalte] = pd.to_datetime(df[datum_spalte], errors="coerce", dayfirst=True)
        energieformen = df.columns.drop(datum_spalte)

        energieform = st.selectbox("🔋 Energieform wählen", energieformen)

        fig = px.line(df, x=datum_spalte, y=energieform,
                      labels={datum_spalte: "Zeitpunkt", energieform: "Leistung (MW)"},
                      title=f"Installierte Leistung – {energieform}")

        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Fehler beim Laden des Moduls 'smard_csv_daten': {e}")
