import pandas as pd
import pathlib
import argparse
import datetime
import requests
import shutil
import zipfile
import io
import os
import streamlit as st
import pydeck as pdk

DEFAULT_DATA_PATH = "data/power_plants_germany.csv"

ENERGY_COLORS = {
    "Wind": [
        (0, 153, 255, 180),
        (51, 181, 255, 180),
        (102, 204, 255, 180),
        (153, 221, 255, 180),
    ],
    "Solar": [
        (255, 204, 0, 180),
        (255, 215, 0, 180),
        (255, 235, 50, 180),
        (255, 255, 102, 180),
    ],
    "Wasserkraft": [
        (0, 102, 204, 180),
        (51, 153, 255, 180),
        (102, 178, 255, 180),
        (153, 204, 255, 180),
    ],
    "Biomasse": [
        (0, 153, 0, 180),
        (51, 204, 51, 180),
        (102, 255, 102, 180),
        (153, 255, 153, 180),
    ],
    "Erdgas": [
        (255, 102, 102, 180),
        (255, 140, 140, 180),
        (255, 178, 178, 180),
        (255, 204, 204, 180),
    ],
    "Kohle": [
        (102, 51, 0, 180),
        (153, 76, 0, 180),
        (204, 102, 0, 180),
        (153, 102, 51, 180),
    ],
    "Kernenergie": [
        (153, 0, 0, 180),
        (204, 0, 0, 180),
        (255, 51, 51, 180),
        (255, 102, 102, 180),
    ],
    "Müll": [
        (102, 102, 102, 180),
        (153, 153, 153, 180),
        (192, 192, 192, 180),
        (224, 224, 224, 180),
    ],
    "Geothermie": [
        (204, 102, 255, 180),
        (221, 153, 255, 180),
        (238, 204, 255, 180),
        (230, 153, 255, 180),
    ],
}

OPS_DATA_URLS = [
    "https://data.open-power-system-data.org/conventional_power_plants/latest/conventional_power_plants_DE.csv",
    "https://data.open-power-system-data.org/renewable_power_plants/latest/renewable_power_plants_DE.csv",
]

COLUMN_MAPPING = {
    "energy_source_level_2": "type",
    "lat": "lat",
    "lon": "lon",
    "capacity_net_bnetza": "capacity_mw",
    "electrical_capacity": "capacity_mw",
}

TYPE_NORMALIZATION = {
    "Natural gas": "Erdgas",
    "Hard coal": "Kohle",
    "Lignite": "Kohle",
    "Nuclear": "Kernenergie",
    "Wind": "Wind",
    "Solar": "Solar",
    "Biomass": "Biomasse",
    "Hydro": "Wasserkraft",
    "Geothermal": "Geothermie",
    "Waste": "Müll",
}

def _download_opsd_csvs():
    df_list = []
    for url in OPS_DATA_URLS:
        resp = requests.get(url)
        resp.raise_for_status()
        df = pd.read_csv(io.StringIO(resp.content.decode("utf-8")))
        print("🔎 CSV Spalten:", df.columns.tolist())
        df_list.append(df)
    return pd.concat(df_list, ignore_index=True)

def _apply_column_mapping(df: pd.DataFrame) -> pd.DataFrame:
    print("📋 Vorhandene Spalten beim Mapping:", df.columns.tolist())
    for old, new in COLUMN_MAPPING.items():
        if old in df.columns:
            df[new] = df[old]
    # Name column prioritization
    name_sources = ["name_bnetza", "block_bnetza", "name_uba", "company", "municipality", "comment"]
    df["name"] = None
    for col in name_sources:
        if col in df.columns:
            df["name"] = df["name"].fillna(df[col])
    df["name"] = df["name"].fillna("").astype(str).str.strip()
    df["name"] = df["name"].replace("", pd.NA).fillna("Unbekannt")
    missing = [v for v in ["name", "type", "lat", "lon", "capacity_mw"] if v not in df.columns]
    if missing:
        raise KeyError(f"Pflichtfeld '{missing[0]}' in CSV nicht gefunden. Header: {list(df.columns)}")
    return df[["name", "type", "lat", "lon", "capacity_mw"]]

def _load_data(path: str) -> pd.DataFrame:
    if not pathlib.Path(path).exists():
        st.error(f"❌ Datei nicht gefunden: {path}")
        return None
    df = pd.read_csv(path)
    df = df.dropna(subset=["lat", "lon", "type"])
    df = df[df["capacity_mw"] > 1]
    df["color"] = df["type"].apply(lambda x: ENERGY_COLORS.get(x, [(128, 128, 128, 180)])[0])
    df["capacity_str"] = df["capacity_mw"].map("{:.2f}".format)
    return df

def _get_mapbox_token():
    try:
        return st.secrets["mapbox"]["token"]
    except Exception:
        st.warning("🔑 Kein Mapbox-Token gefunden. Bitte in .streamlit/secrets.toml eintragen.")
        return ""

def _build_deck(df, selection, mapbox_token, tooltip_field="name"):
    pdk.settings.mapbox_api_key = mapbox_token  # ⬅️ Mapbox-Token korrekt setzen
    filtered = df[df["type"].isin(selection)]

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered,
        get_position='[lon, lat]',
        get_color='color',
        get_radius=5000,
        pickable=True,
    )

    deck = pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        layers=[layer],
        initial_view_state=pdk.ViewState(
            latitude=51,
            longitude=10,
            zoom=5,
            pitch=0,
        ),
        tooltip={"text": f"{{{tooltip_field}}} ({{type}})\n{{capacity_str}} MW"},
    )
    return deck
    return pdk.Deck(
        map_style="mapbox://styles/mapbox/light-v9",
        layers=[layer],
        initial_view_state=view_state,
        tooltip={"text": "{name} ({type})\n{capacity_mw} MW"},
        mapbox_key=mapbox_token,
    )
def _save_to_csv(df: pd.DataFrame, path: str):
    os.makedirs(pathlib.Path(path).parent, exist_ok=True)
    df.to_csv(path, index=False)

def _load_opsd():
    df = _download_opsd_csvs()
    df = _apply_column_mapping(df)
    df = df.dropna(subset=["lat", "lon", "type"])
    df = df[df["capacity_mw"] > 1]
    df["type"] = df["type"].replace(TYPE_NORMALIZATION)
    return df

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", choices=["opsd"], default="opsd")
    args = parser.parse_args()

    if args.source == "opsd":
        df = _load_opsd()
    else:
        raise NotImplementedError("Nur OPSD wird aktuell unterstützt.")

    df = df[["name", "type", "lat", "lon", "capacity_mw"]]
    _save_to_csv(df, DEFAULT_DATA_PATH)
    print(f"✅ Gespeichert: {DEFAULT_DATA_PATH} ({len(df):,} Einträge)")
    print(f"Stand der Liste: {datetime.date.today()}")

if __name__ == "__main__":
    main()
