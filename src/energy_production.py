import streamlit as st
import pandas as pd
import subprocess
import pathlib
import pydeck as pdk
from watermarks import set_watermark


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
    set_watermark("images/watermark/chargingpoints_pic.png")
    #set_watermark("src/images/watermark/chargingpoints_pic.png")
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

    # Gesamtleistung pro Energieform
    df_selection = df[df["type"].isin(selection)]
    leistung_summary = (
        df_selection.groupby("type")["capacity_mw"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )
    gesamtleistung_mw = leistung_summary["capacity_mw"].sum()
    st.metric("Gesamtleistung (MW)", f"{gesamtleistung_mw:,.0f} MW")
    st.subheader("🔋 Gesamtleistung nach Energieform")
    leistung_summary["capacity_mw"] = leistung_summary["capacity_mw"].map(lambda x: f"{x:,.2f} MW")
    st.dataframe(leistung_summary.rename(columns={"type": "Energieform", "capacity_mw": "Gesamtleistung"}))

    deck = _build_deck(df, selection, mapbox_token, tooltip_field="name")
    st.pydeck_chart(deck, use_container_width=True)

    with st.expander("🗂️ Legende"):
        st.markdown(
            "In der Karte sind die Kraftwerke farblich nach Energieform codiert. "
            "Die folgende Übersicht zeigt, welcher Farbe welche Energieform entspricht:"
        )
        legend_df = pd.DataFrame({
            "Energieform": list(ENERGY_COLORS.keys()),
            "Farbcode (RGBA)": list(ENERGY_COLORS.values())
        })

        st.markdown("#### Farblegende (Farbzuordnung je Energieform)")
        for _, row in legend_df.iterrows():
            rgba = row['Farbcode (RGBA)']
            farben = rgba if isinstance(rgba[0], (list, tuple)) else [rgba]
            leistungsklassen = ["unter 5 MW", "5–20 MW", "20–100 MW", "über 100 MW"]
            farbpunkte = "".join([
                f"<span title='{row['Energieform']} mit Leistung {leistungsklassen[i]}' "
                f"style='display:inline-block; width:16px; height:16px; margin-right:4px; "
                f"background-color:rgba({r},{g},{b},{a / 255}); border-radius:50%; border:1px solid #ccc;'></span>"
                for i, (r, g, b, a) in enumerate(farben)
            ])

            st.markdown(
                f"<div style='margin: 6px 0; display:flex; align-items:center;'>"
                f"<span style='width:120px;'>{row['Energieform']}</span>"
                f"{farbpunkte}"
                f"</div>",
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    run()
