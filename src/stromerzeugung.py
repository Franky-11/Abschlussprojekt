

"""
stromerzeugung.py – Streamlit‑Seite „Stromerzeugung“

Dieses Modul liefert:
  • run()          – Haupteinstieg für das Dashboard
  • st_display()   – UI‑Funktion (identisch zu run, aber separat nutzbar)
  • get_smard_data() – Holt optionale Live‑Daten von SMARD
"""

from pathlib import Path
import io
import requests
import pandas as pd
import plotly.express as px
import streamlit as st
import pydeck as pdk  # Mapbox/DeckGL‑Layer für die Karte

# ----------------------------------------------------------------------------- 
# Mapbox‑Token – direkt gesetzt (vom Nutzer bereitgestellt)
# -----------------------------------------------------------------------------
MAPBOX_TOKEN = "pk.eyJ1IjoiemlneXRiMDA3IiwiYSI6ImNtY2IyNnFsYTBiMzEya3NiMjIwZTVka2IifQ.vII9n9yQK7xKjyFemuiyug"

# pydeck & plotly verwenden diesen globalen Env‑Key
import os
os.environ["MAPBOX_API_KEY"] = MAPBOX_TOKEN
os.environ["MAPBOX_ACCESS_TOKEN"] = MAPBOX_TOKEN

# ----------------------------------------------------------------------------- 
# Datenquellen
# -----------------------------------------------------------------------------
DATA_DIR = Path(__file__).parent / "data"          # ../data

@st.cache_data(show_spinner=False)
def load_generation_data(csv: str = "generation.csv") -> pd.DataFrame:
    """
    Lokale CSV mit Zeitreihen der Strom­erzeugung laden.
    Erwartet Spalte 'timestamp' + beliebige Techno­logie‑Spalten.
    """
    file_path = DATA_DIR / csv
    if file_path.exists():
        df = pd.read_csv(file_path, parse_dates=["timestamp"])
        df.set_index("timestamp", inplace=True)
    else:
        # Fallback – Dummy‑Daten (damit die Seite auch ohne Datei funktioniert)
        rng = pd.date_range("2025-01-01", periods=24, freq="h")
        df = pd.DataFrame(
            {"wind": 0, "solar": 0, "gas": 0, "biomass": 0}, index=rng
        )
    return df


def calculate_generation_mix(df: pd.DataFrame) -> pd.DataFrame:
    """Anteil je Technologie in Prozent."""
    mix = df.div(df.sum(axis=1), axis=0) * 100
    return mix.round(2)


# ----------------------------------------------------------------------------- 
# Optional: Live‑Daten von SMARD laden
# -----------------------------------------------------------------------------
def get_smard_data(local_csv: str = "smard_verbrauch_erzeugung.csv"):
    """
    Versucht zuerst, eine lokale SMARD‑CSV aus dem data‑Ordner zu laden.
    Falls sie fehlt, wird ein Online‑Download der offiziellen SMARD‑Datei
    (Verbrauch & Erzeugung, Deutschland gesamt) für den aktuellen Monat
    versucht.  Schlägt auch das fehl, liefert die Funktion Dummy‑Daten,
    damit das Dashboard nicht abstürzt.

    Rückgabe:
        latest_ts (pd.Timestamp)
        need_df   (DataFrame, letzte 24 h Verbrauch)
        gen_df    (DataFrame, letzte 24 h Erzeugung)
    """
    try:
        file_path = DATA_DIR / local_csv
        if file_path.exists():
            # 1️⃣ Lokale Datei verwenden
            smard = pd.read_csv(file_path, sep=";", decimal=",")
        else:
            # 2️⃣ Online‑Fallback
            import datetime, urllib.request
            today = datetime.date.today()
            url = (
                "https://www.smard.de/nip-download-manager-download/106/DE_all/"
                f"{today.year}_{today.month:02d}_Verbrauch_Erzeugung.csv"
            )
            with urllib.request.urlopen(url, timeout=10) as resp:
                smard = pd.read_csv(resp, sep=";", decimal=",")
        # Daten aufbereiten
        smard["timestamp"] = pd.to_datetime(smard["Datum"] + " " + smard["Zeit"])
        latest_ts = smard["timestamp"].max()

        need_df = (
            smard[["timestamp", "Verbrauch"]]
            .set_index("timestamp")
            .sort_index()
            .tail(24)
        )
        gen_df = (
            smard[["timestamp", "Erzeugung"]]
            .set_index("timestamp")
            .sort_index()
            .tail(24)
        )
        return latest_ts, need_df, gen_df

    except Exception:
        # 3️⃣ Dummy‑Daten als sichere Rückfall‑Option
        rng = pd.date_range("2025-01-01", periods=24, freq="h")
        dummy = pd.DataFrame({"Verbrauch": 0, "Erzeugung": 0}, index=rng)
        latest_ts = rng[-1]
        return latest_ts, dummy[["Verbrauch"]], dummy[["Erzeugung"]]


# ----------------------------------------------------------------------------- 
# Streamlit‑UI
# -----------------------------------------------------------------------------
def st_display():
    st.title("Stromerzeugung :material/charging_station:")

    # Headerbild
    col1, col2 = st.columns([1, 1])
    with col2:
        st.image("images/power-lines-1809237_1920.jpg", use_container_width=True)
    st.divider()

    # Daten einlesen & auswerten
    raw = load_generation_data()
    mix = calculate_generation_mix(raw)

    techs = st.multiselect(
        "Technologien auswählen", options=mix.columns, default=list(mix.columns)
    )
    fig = px.area(mix[techs], title="Erzeugungsmix (%)", labels={"value": "%"})
    st.plotly_chart(fig, use_container_width=True)

    # -----------------------------------------------------------------
    # 🔍 Schnelltest: Mapbox‑Karte anzeigen, sofern Token vorhanden
    # -----------------------------------------------------------------
    if MAPBOX_TOKEN:
        st.markdown("### Testkarte (Mapbox)")
        # Minimale Daten: Mittelpunkt Deutschland
        map_df = pd.DataFrame({"lat": [51.1657], "lon": [10.4515]})
        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_df,
            get_position="[lon, lat]",
            get_radius=50000,
            get_fill_color=[255, 0, 0, 160],
        )
        view_state = pdk.ViewState(latitude=51.1657, longitude=10.4515, zoom=4)
        st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))
    else:
        st.info(
            "Kein MAPBOX_TOKEN gefunden (secrets.toml oder Umgebungsvariable). "
            "Karte wird nicht angezeigt."
        )

    st.subheader("Rohdaten (letzte 48 Zeitschritte)")
    st.dataframe(raw.tail(48))


# Alias für das Dashboard
def run():
    st_display()
