import streamlit as st
import pandas as pd
import subprocess
import pathlib
import pydeck as pdk

from fetch_power_plants import (
    DEFAULT_DATA_PATH,
    ENERGY_COLORS,
    _get_mapbox_token,
    _load_data,
    _build_deck,
)

def _fetch_data():
    with st.spinner("Lade aktuelle Kraftwerksdaten von Open Power System Data…"):
        try:
            script_path = pathlib.Path(__file__).parent / "fetch_power_plants.py"
            subprocess.run(["python", str(script_path), "--source", "opsd"], check=True)
            st.success("✅ Daten erfolgreich geladen.")
        except subprocess.CalledProcessError as e:
            st.error("❌ Fehler beim Abrufen der Daten.")
            st.exception(e)

def run():
    st.title("🗺️ Energielandkarte Deutschlands")
    st.caption("Interaktive Übersicht aller Stromerzeugungsanlagen – filterbar nach Energieform.")

    mapbox_token = _get_mapbox_token()
    pdk.settings.mapbox_api_key = mapbox_token  # ✅ Mapbox API-Key für pydeck setzen

    st.sidebar.header("⚙️ Einstellungen")
    if st.sidebar.button("🔄 Kraftwerksdaten abrufen"):
        _fetch_data()

    data_path = st.sidebar.text_input("Pfad zur Kraftwerks-CSV", value=DEFAULT_DATA_PATH)
    df = _load_data(data_path)
    if df is None or df.empty:
        st.stop()

    energy_types = sorted(df["type"].unique())
    default_sel = [e for e in energy_types if e in {"Wind", "Solar"}] or energy_types
    selection = st.sidebar.multiselect("Energieformen auswählen", energy_types, default=default_sel)

    if not selection:
        st.info("Bitte mindestens eine Energieform auswählen.")
        st.stop()

    deck = _build_deck(df, selection, mapbox_token)
    st.pydeck_chart(deck, use_container_width=True)

    with st.expander("🗂️ Legende"):
        st.dataframe(pd.DataFrame({
            "Energieform": list(ENERGY_COLORS.keys()),
            "Farbe (RGBA)": list(ENERGY_COLORS.values())
        }))

if __name__ == "__main__":
    run()
