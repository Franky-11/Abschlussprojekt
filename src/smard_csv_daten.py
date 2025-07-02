import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path

# ────────────────────────────────────────────────────────────────
# Helfer
# ────────────────────────────────────────────────────────────────
def _time_cols(df: pd.DataFrame) -> list[str]:
    """Spaltennamen, die Datum/Zeit enthalten."""
    return [c for c in df.columns if any(k in c.lower() for k in ("datum", "zeit"))]

def _clean_number(series: pd.Series) -> pd.Series:
    """Deutsch formatierte Zahl → float."""
    return (
        series.astype(str)
        .str.replace(".", "", regex=False)      # Tausenderpunkt
        .str.replace(",", ".", regex=False)    # Komma → Punkt
        .astype(float, errors="ignore")
    )

def _list_smard_csvs(folder: Path) -> list[Path]:
    return sorted(folder.glob("*.csv"))

def _energy_cols(df: pd.DataFrame, time_cols: list[str]) -> list[str]:
    """Alle Nicht‑Zeit‑Spalten, die mindestens einen numerischen Wert enthalten."""
    cols = []
    for c in df.columns:
        if c in time_cols:
            continue
        ser = _clean_number(df[c])
        if ser.notna().any():
            cols.append(c)
    return cols

# ────────────────────────────────────────────────────────────────
# Haupt‑App
# ────────────────────────────────────────────────────────────────
def run() -> None:
    st.title("📊 SMARD‑Auswertung: installierte Leistung / Erzeugung / Verbrauch")

    smard_path = Path("data/smard")
    if not smard_path.exists():
        st.error("📂 Ordner `data/smard/` nicht gefunden.")
        return

    files = _list_smard_csvs(smard_path)
    if not files:
        st.error("Keine SMARD‑CSV‑Dateien im Ordner `data/smard/` gefunden.")
        return

    # Datei wählen
    st.sidebar.subheader("⚙️ Dateiauswahl")
    file_display = {f.name: f for f in files}
    file_name = st.sidebar.selectbox("CSV wählen", list(file_display.keys()))
    csv_file = file_display[file_name]

    # CSV laden
    try:
        df_raw = pd.read_csv(csv_file, sep=";", encoding="utf-8")
    except Exception as exc:
        st.error("❌ CSV kann nicht gelesen werden.")
        st.exception(exc)
        return

    time_cols = _time_cols(df_raw)
    if not time_cols:
        st.error("❌ Keine Datum-/Zeitspalte gefunden.")
        return

    df = df_raw.copy()
    for col in time_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
    df = df.dropna(subset=time_cols).sort_values(time_cols[0])

    energy_cols = _energy_cols(df, time_cols)
    if not energy_cols:
        st.error("❌ In dieser Datei keine Energie-Spalten entdeckt.")
        return

    df[energy_cols] = df[energy_cols].apply(_clean_number, axis=0)

    # UI
    min_d, max_d = df[time_cols[0]].dt.date.min(), df[time_cols[0]].dt.date.max()
    st.sidebar.subheader("📅 Zeitraum")
    start_d, end_d = st.sidebar.date_input(
        "Von – Bis", (min_d, max_d), min_value=min_d, max_value=max_d
    )
    if isinstance(start_d, tuple):  # ältere Streamlit-Version
        start_d, end_d = start_d

    mask = (df[time_cols[0]].dt.date >= start_d) & (df[time_cols[0]].dt.date <= end_d)
    df_time = df.loc[mask]

    st.sidebar.subheader("🔋 Energieformen")
    sel_energy = st.sidebar.multiselect(
        "Spalten auswählen", options=energy_cols, default=energy_cols[:3]
    )
    if not sel_energy:
        st.info("Bitte mindestens eine Energieform auswählen.")
        return

    chart_kind = st.sidebar.radio("Diagramm-Typ", ["Linie", "Gestapelte Fläche"])

    # Diagramm
    st.subheader(f"Datei: {csv_file.name}")
    if chart_kind == "Linie":
        fig = px.line(
            df_time,
            x=time_cols[0],
            y=sel_energy,
            labels={time_cols[0]: "Zeitpunkt", "value": "MW", "variable": "Energieform"},
        )
    else:
        df_m = df_time.melt(id_vars=time_cols, value_vars=sel_energy)
        fig = px.area(
            df_m,
            x=time_cols[0],
            y="value",
            color="variable",
            labels={time_cols[0]: "Zeitpunkt", "value": "MW", "variable": "Energieform"},
        )
    fig.update_layout(hovermode="x unified", legend_title_text="Energieform")
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("🧾 Spalten der Datei"):
        st.write(list(df_raw.columns))

if __name__ == "__main__":  # Direkt‑Start zu Test­zwecken
    import streamlit.web.bootstrap as boot
    boot.run(__file__, f"run.py {__file__}", [])
