import streamlit as st
import pandas as pd
import plotly.express as px
import os
from pathlib import Path
from watermarks import set_watermark


# ────────────────────────────────────────────────────────────────
# Helfer
# ────────────────────────────────────────────────────────────────
def _time_cols(df: pd.DataFrame) -> list[str]:
    """Spaltennamen, die Datum/Zeit enthalten."""
    return [c for c in df.columns if any(k in c.lower() for k in ("datum", "zeit"))]

def _clean_number(series: pd.Series) -> pd.Series:
    """Deutsch formatierte Zahl → float."""
    return pd.to_numeric(series.astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False),
        errors="coerce"
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
    set_watermark("images/watermark/chargingpoints_pic.png")
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
    display_names = {}
    for f in files:
        name = f.name
        if "Installierte" in name:
            label = "Installierte"
        elif "Realisierte" in name:
            label = "Realisierte"
        elif "Prognostizierter" in name:
            label = "Prognostizierter"
        elif "Ausgleichsenergie" in name:
            label = "Ausgleichsenergie"
        else:
            label = f.stem.split("_")[0]
        display_names[name] = label
    display_to_file = {v: k for k, v in display_names.items()}
    file_display_short = {v: file_display[k] for v, k in display_to_file.items()} if 'file_display' in locals() else {v: f for v, f in zip(display_to_file.keys(), files)}
    selected_display_name = st.sidebar.selectbox("CSV wählen", list(file_display_short.keys()))
    file_name = display_to_file[selected_display_name]
    csv_file = file_display_short[selected_display_name]

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
    if "federal_state" in df.columns:
        df["federal_state"] = df["federal_state"].astype(str)
    for col in time_cols:
        df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
    df = df.dropna(subset=time_cols).sort_values(time_cols[0])

    energy_cols = _energy_cols(df, time_cols)
    if not energy_cols:
        st.error("❌ In dieser Datei keine Energie-Spalten entdeckt.")
        return

    df[energy_cols] = df[energy_cols].apply(_clean_number, axis=0)

    st.sidebar.subheader("🗺️ Region")
    if "federal_state" in df.columns:
        sel_state = st.sidebar.selectbox("Bundesland filtern (optional)", ["Alle"] + sorted(df["federal_state"].dropna().unique()))
        if sel_state != "Alle":
            df = df[df["federal_state"] == sel_state]
            df_time = df_time[df_time["federal_state"] == sel_state]

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
    st.sidebar.subheader("⚙️ Weitere Optionen")
    smooth = st.sidebar.checkbox("🔄 Gleitender Mittelwert (3 Werte)")
    compare = st.sidebar.checkbox("📉 Vergleich mit zweitem Zeitraum")

    COLORS = px.colors.qualitative.Plotly

    def plot_energy(df_plot, title_suffix=""):
        if chart_kind == "Linie":
            fig = px.line(
                df_plot,
                x=time_cols[0],
                y=sel_energy,
                labels={time_cols[0]: "Zeitpunkt", "value": "MW", "variable": "Energieform"},
                color_discrete_sequence=COLORS
            )
        else:
            df_m = df_plot.melt(id_vars=time_cols, value_vars=sel_energy)
            fig = px.area(
                df_m,
                x=time_cols[0],
                y="value",
                color="variable",
                labels={time_cols[0]: "Zeitpunkt", "value": "MW", "variable": "Energieform"},
                color_discrete_sequence=COLORS
            )
        fig.update_layout(
            title=f"Energieproduktion {title_suffix}",
            hovermode="x unified",
            legend_title_text="Energieform"
        )
        return fig

    # Glätten
    if smooth:
        df_time[sel_energy] = df_time[sel_energy].rolling(window=3, min_periods=1).mean()

    # Hauptplot

    # Aggregierte Leistung (MWh)
    st.subheader("📊 Gesamtleistung im gewählten Zeitraum")
    df_sum = df_time[sel_energy].sum().sort_values(ascending=False)
    df_sum_table = pd.DataFrame({
        "Energieform": df_sum.index,
        "Gesamt [MWh]": df_sum.values
    })
    df_sum_table["Gesamt [MWh]"] = df_sum_table["Gesamt [MWh]"].apply(lambda x: f"{x:,.0f}".replace(",", "."))
    st.dataframe(df_sum_table, hide_index=True, use_container_width=True)

    st.subheader(f"Datei: {selected_display_name}")
    with st.expander("🛈 Erklärung zur Datei und Auswertung", expanded=False):
        base_text = """
        Diese Auswertung visualisiert die zeitliche Entwicklung der ausgewählten Energieformen 
        im angegebenen Zeitraum. Jede CSV-Datei enthält spezifische Daten aus dem SMARD-Portal, 
        z. B. zur installierten Leistung, Stromerzeugung oder dem Verbrauch je Energieform. 

        Die Diagramme zeigen aggregierte Werte im Viertelstundenraster (15 min) – summiert ergibt sich daraus die Gesamtmenge in MWh. 
        Mit dem Vergleichszeitraum lassen sich Entwicklungen analysieren.
        """

        explanation_map = {
            "Ausgleichsenergie": "Für das ausgewählte Diagramm (Ausgleichsenergie) bedeutet dies:\n\nDiese Datei zeigt den Ausgleich von Differenzen zwischen prognostiziertem und realisiertem Strombedarf. Sie gibt Aufschluss über Lastabweichungen im Netz sowie deren Volumen und Preisentwicklung.",
            "Installierte": "Für das ausgewählte Diagramm (Installierte Leistung) bedeutet dies:\n\nDiese Datei enthält Informationen über die installierte Leistung in MW, gegliedert nach Energieform. Sie spiegelt die theoretische Erzeugungskapazität wider.",
            "Realisierte": "Für das ausgewählte Diagramm (Realisierte Erzeugung) bedeutet dies:\n\nDiese Datei zeigt die tatsächlich erzeugte Strommenge über den betrachteten Zeitraum. Die Werte basieren auf Messungen und spiegeln die reale Einspeisung wider.",
            "Prognostizierter": "Für das ausgewählte Diagramm (Prognostizierter Verbrauch) bedeutet dies:\n\nDiese Datei enthält prognostizierte Werte zur Stromnachfrage und -erzeugung. Sie dient zur Planung und Koordination im Stromnetz."
        }

        for key, text in explanation_map.items():
            if key.lower() in selected_display_name.lower():
                st.markdown(base_text + "\n\n" + text)
                break
        else:
            st.markdown(base_text)
    fig_main = plot_energy(df_time)
    st.plotly_chart(fig_main, use_container_width=True)

    # Vergleichszeitraum
    if compare:
        st.sidebar.subheader("📅 Vergleichszeitraum")
        date_input = st.sidebar.date_input(
            "Vergleich: Von – Bis", (min_d, max_d), min_value=min_d, max_value=max_d
        )
        if isinstance(date_input, tuple) and len(date_input) == 2:
            comp_start, comp_end = date_input
        else:
            st.error("❌ Bitte wählen Sie ein Start- und ein Enddatum für den Vergleichszeitraum.")
            return
        mask_comp = (df[time_cols[0]].dt.date >= comp_start) & (df[time_cols[0]].dt.date <= comp_end)
        df_comp = df.loc[mask_comp].copy()
        if smooth:
            df_comp[sel_energy] = df_comp[sel_energy].rolling(window=3, min_periods=1).mean()
        fig_comp = plot_energy(df_comp, title_suffix="(Vergleich)")
        st.plotly_chart(fig_comp, use_container_width=True)

    with st.expander("🧾 Spalten der Datei"):
        st.write(list(df_raw.columns))

if __name__ == "__main__":  # Direkt‑Start zu Test­zwecken
    import streamlit.web.bootstrap as boot
    boot.run(__file__, f"run.py {__file__}", [])
