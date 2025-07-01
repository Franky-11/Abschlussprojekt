
import requests
import pandas as pd
from datetime import datetime, timedelta

ENERGY_SOURCES = {
    "solar": 4068,
    "wind_onshore": 4067,
    "wind_offshore": 1225,
    "biomass": 4066,
    "hydro": 1226,
    "fossil": 1227,
    "other_renewables": 1228,
}

def fetch_smard_data(filter_id: int, region_id: int = 122) -> pd.DataFrame:
    now = datetime.utcnow() - timedelta(minutes=60)
    start_time = now - timedelta(hours=48)
    start_timestamp = int(start_time.timestamp() * 1000)

    url = f"https://www.smard.de/app/chart_data/{filter_id}/{region_id}/{filter_id}_{region_id}_quarterhour_{start_timestamp}.json"
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        raw_data = resp.json().get("values", [])
        records = [(datetime.utcfromtimestamp(ts / 1000), val) for ts, val in raw_data if val is not None]
        return pd.DataFrame(records, columns=["timestamp", "value"])
    except Exception as e:
        print(f"⚠️ Fehler beim Abruf von SMARD-Daten ({filter_id}): {e}")
        return pd.DataFrame(columns=["timestamp", "value"])

def update_all_sources() -> pd.DataFrame | None:
    combined = None
    for name, fid in ENERGY_SOURCES.items():
        df = fetch_smard_data(fid)
        if not df.empty:
            df = df.rename(columns={"value": name})
            if combined is None:
                combined = df
            else:
                combined = pd.merge(combined, df, on="timestamp", how="outer")
    if combined is not None:
        combined = combined.sort_values("timestamp").fillna(0)
        combined.set_index("timestamp", inplace=True)
    return combined
