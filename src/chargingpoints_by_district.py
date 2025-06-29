# chargingpoints_by_district_expanded2.py
# Streamlit-App: Deutsche Ladepunkteinfrastruktur
# ----------------------------------------------------------------------
import streamlit as st
from streamlit_folium import st_folium
import pandas as pd
import json
import folium
from folium import Element
import branca.colormap as cm
from folium.plugins import DualMap
from dateutil.relativedelta import relativedelta
import plotly.express as px


# ---------- Seiteneinstellungen ----------------------------------------
try:
    st.set_page_config(page_title="Ladepunkteinfrastruktur", layout="wide")
except Exception:
    pass

# ---------- Titelbereich ------------------------------------------------
col1, col2 = st.columns([1, 1])
with col1:
    st.title("Ladepunkteinfrastruktur :material/ev_station:")
    st.write("***Gesamt:*** 169.082 Ladepunkte")
    st.write("***Normalladepunkte:*** 129.450")
    st.write("***Schnellladepunkte:*** 39.632")
    st.write("***Wallboxen:*** 1 Mio.")
with col2:
    st.image("charging-station-4636710_1920.jpg", use_container_width=True)
st.divider()

# ---------- Daten einlesen ----------------------------------------------
pfad_lp = "data/Ladesaeulenregister_BNetzA.csv"
try:
    df_lp = pd.read_csv(pfad_lp, sep=";", engine="python", encoding="latin-1", on_bad_lines="warn", dtype=str)
except:
    df_lp = pd.read_csv(pfad_lp, sep=";", engine="python", encoding="latin-1", dtype=str)
# Datum und Koordinaten
df_lp["Inbetriebnahmedatum"] = pd.to_datetime(df_lp.get("Inbetriebnahmedatum"), dayfirst=True, errors='coerce')
df_lp["Anzahl Ladepunkte"] = df_lp["Anzahl Ladepunkte"].str.replace(",", "").astype(int)
for c in ["Breitengrad", "Längengrad"]:
    df_lp[c] = df_lp[c].str.replace(",", ".").astype(float)

# BEV/Ladepunkt-Daten
df_bev_lp = pd.read_csv("data/df_lade_bev.csv", sep=",", encoding="latin-1")
df_bev_lp["RS"] = df_bev_lp["Kreis_code"].astype(str).str.zfill(5)
if "BEV_pro_Ladepunkt" in df_bev_lp.columns:
    df_bev_lp["EV_per_LP"] = df_bev_lp["BEV_pro_Ladepunkt"].astype(float)
else:
    st.error("Spalte 'BEV_pro_Ladepunkt' nicht gefunden in df_lade_bev.csv.")
    st.stop()

# GeoJSONs laden
with open("data/landkreise.geojson", encoding="utf-8") as f:
    geo_lp = json.load(f)
with open("data/landkreise_simplify200.geojson", encoding="utf-8") as f:
    geo_bev_lp = json.load(f)

# ---------- Aggregation & Enrichment ------------------------------------
# Linke Karte: Ladepunkte je Landkreis
df_counts = df_lp.groupby("Kreis_kreisfreie_Stadt")["Anzahl Ladepunkte"].sum().reset_index(name="Lp_summe")
lookup_lp = dict(zip(df_counts["Kreis_kreisfreie_Stadt"], df_counts["Lp_summe"]))
for feat in geo_lp["features"]:
    bez = feat["properties"].get("BEZ","").strip()
    gen = feat["properties"].get("GEN","").strip()
    key = f"{bez} {gen}".strip()
    feat["properties"]["Lp_summe"] = lookup_lp.get(key, 0)
    feat["properties"]["LABEL"] = key

# Rechte Karte: EV pro Ladepunkt je Landkreis
lookup_ev = dict(zip(df_bev_lp["RS"], df_bev_lp["EV_per_LP"]))
for feat in geo_bev_lp["features"]:
    rs = feat["properties"].get("RS","")
    feat["properties"]["EV_per_LP"] = lookup_ev.get(rs, 0)
    bez = feat["properties"].get("BEZ","").strip()
    gen = feat["properties"].get("GEN","").strip()
    feat["properties"]["LABEL"] = f"{bez} {gen}".strip()

# ---------- Filterfelder in zwei Spalten unterteilen -----------------------------
col_f1, col_f2 = st.columns(2)
with col_f1:
    st.subheader("Landkreisfilter: Ladepunkte")
    min_lp, max_lp = df_counts["Lp_summe"].min(), df_counts["Lp_summe"].max()
    sel_min_lp = st.number_input(
        "Min Ladepunkte:",
        min_value=int(min_lp),
        max_value=int(max_lp),
        value=int(min_lp)
    )
    sel_max_lp = st.number_input(
        "Max Ladepunkte:",
        min_value=int(min_lp),
        max_value=int(max_lp),
        value=int(max_lp)
    )
with col_f2:
    st.subheader("Filter: EV pro Ladepunkt")
    min_ev, max_ev = df_bev_lp["EV_per_LP"].min(), df_bev_lp["EV_per_LP"].max()
    ev_min, ev_max = st.slider(
        "EV pro Ladepunkt Bereich:",
        min_value=float(min_ev),
        max_value=float(max_ev),
        value=(float(min_ev), float(max_ev)),
        step=(float(max_ev) - float(min_ev)) / 100
    )

# ---------- Farbskalen -------------------------------------------------- --------------------------------------------------
max_lp = int(df_counts["Lp_summe"].max())
scale_lp = cm.StepColormap(
    colors=["#ffffff","#deebf7","#9ecae1","#3182bd","#08519c"],
    index=[0,99,149,249,1999, max_lp],
    caption="Ladepunkte je Landkreis"
)
max_ev = float(df_bev_lp["EV_per_LP"].max())
# manuelle Klassenschwellen ohne inf, letzte Stufe bis max_ev
scale_ev = cm.StepColormap(
    colors=['#00441b','#238b45','#66c2a4','#ffffff','#fdae6b','#e34a33','#b30000'],
    index=[2,5,8,11,14,17,21, max_ev],
    caption="EV pro Ladepunkt"
)

# ---------- Synchronisierte Karten mit DualMap --------------------------- ---------------------------
# Erzeuge DualMap ohne voreingestellte Tiles
dual = DualMap(location=[51,9.5], zoom_start=6)
# Hintergrund-Tiles für beide Karten
folium.TileLayer('cartodbpositron', name='Basemap').add_to(dual.m1)
folium.TileLayer('cartodbpositron', name='Basemap').add_to(dual.m2)
# Linke Karte-Layer (Ladepunkte) (Ladepunkte)
folium.GeoJson(
    geo_lp,
    style_function=lambda ft: {
        'fillColor': scale_lp(ft['properties']['Lp_summe']),
        'fillOpacity': 0.8 if sel_min_lp <= ft['properties']['Lp_summe'] <= sel_max_lp else 0.2,
        'color': 'black', 'weight': 1
    },
    tooltip=folium.GeoJsonTooltip(['LABEL','Lp_summe'], ['', 'Ladepunkte:'], localize=True)
).add_to(dual.m1)
# entferne automatische Legende
# scale_lp.add_to(dual.m1)
# Rechte Karte-Layer (EV pro LP)
folium.GeoJson(
    geo_bev_lp,
    style_function=lambda ft: {
        'fillColor': scale_ev(ft['properties']['EV_per_LP']),
        'fillOpacity': 0.8 if ev_min <= ft['properties']['EV_per_LP'] <= ev_max else 0.2,
        'color': 'black', 'weight': 1
    },
    tooltip=folium.GeoJsonTooltip(['LABEL','EV_per_LP'], ['', 'EV/LP:'], localize=True)
).add_to(dual.m2)
# entferne automatische Legende
# scale_ev.add_to(dual.m2)
# Manuelle HTML-Legenden für linke und rechte Karte
legend_html_lp = '''
<div style="position: absolute; top: 120px; left: 10px; z-index:9999; background: rgba(0,0,0,0.7); color: white; padding: 6px; border-radius:4px; font-size:12px; line-height:1.2; max-width:150px; white-space: normal;
overflow-wrap: break-word;
">
  <strong style="display:block; margin-bottom:4px;">Ladepunkte je Landkreis</strong>
  <i style="background:#08519c;width:14px;height:14px;display:inline-block;margin-right:6px;"></i> ≥2000<br>
  <i style="background:#3182bd;width:14px;height:14px;display:inline-block;margin-right:6px;"></i> 250–1999<br>
  <i style="background:#9ecae1;width:14px;height:14px;display:inline-block;margin-right:6px;"></i> 150–249<br>
  <i style="background:#deebf7;width:14px;height:14px;display:inline-block;margin-right:6px;"></i> 100–149<br>
  <i style="background:#ffffff;width:14px;height:14px;display:inline-block;margin-right:6px; border:1px solid #999;"></i> 0–99
</div>
'''
legend_html_ev = '''
<div style="position: absolute; top: 120px; left: calc(50% + 10px); z-index:9999; background: rgba(0,0,0,0.7); color: white; padding: 6px; border-radius:4px; font-size:12px; line-height:1.2; max-width:150px; white-space: normal;
overflow-wrap: break-word;
">
  <strong style="display:block; margin-bottom:4px;">EV pro Ladepunkt</strong>
  <i style="background:#a63603;width:14px;height:14px;display:inline-block;margin-right:6px;"></i> ≥21<br>
  <i style="background:#e6550d;width:14px;height:14px;display:inline-block;margin-right:6px;"></i> 17–21<br>
  <i style="background:#fdae6b;width:14px;height:14px;display:inline-block;margin-right:6px;"></i> 14–17<br>
  <i style="background:#ffffff;width:14px;height:14px;display:inline-block;margin-right:6px; border:1px solid #999;"></i> 11–14<br>
  <i style="background:#66c2a4;width:14px;height:14px;display:inline-block;margin-right:6px;"></i> 8–11<br>
  <i style="background:#238b45;width:14px;height:14px;display:inline-block;margin-right:6px;"></i> 5–8<br>
  <i style="background:#00441b;width:14px;height:14px;display:inline-block;margin-right:6px;"></i> 2–5
</div>
'''
# Füge Legenden vor Rendern hinzu
dual.m1.get_root().html.add_child(Element(legend_html_lp))
dual.m2.get_root().html.add_child(Element(legend_html_ev))
# Render DualMap synchronisiert
st_folium(dual, width="100%", height=600)

# ---------- Top-10 Balkendiagramm Neubauten --------------------------------
st.divider()
st.subheader("Neubauten von Ladepunkten nach Landkreis")
# Zeitfenster-Auswahl
period = st.selectbox(
    "Zeitraum:",
    options=["3 Monate", "6 Monate", "1 Jahr", "2 Jahre"],
    index=1
)
# Berechne cutoff-Datum
now = pd.Timestamp.today()
if period == "3 Monate":
    cutoff = now - relativedelta(months=3)
elif period == "6 Monate":
    cutoff = now - relativedelta(months=6)
elif period == "1 Jahr":
    cutoff = now - relativedelta(years=1)
else:
    cutoff = now - relativedelta(years=2)
# Filter Daten nach Inbetriebnahmedatum und Landkreisfilter
df_new = df_lp[df_lp["Inbetriebnahmedatum"] >= cutoff].copy()
# Anwenden der bestehenden Landkreis-Filter (sel_min_lp, sel_max_lp und ev_min, ev_max)
# Bestimme gültige Kreise
valid_lp = df_counts[
    (df_counts["Lp_summe"] >= sel_min_lp) & (df_counts["Lp_summe"] <= sel_max_lp)
]["Kreis_kreisfreie_Stadt"]
valid_ev = [feat["properties"]["LABEL"] for feat in geo_bev_lp["features"]
            if ev_min <= feat["properties"]["EV_per_LP"] <= ev_max]
# Filter df_new auf gültige Kreise
df_new = df_new[df_new["Kreis_kreisfreie_Stadt"].isin(valid_lp)]
# Gruppieren und zählen Ladepunkte-Neubauten (Anzahl Ladepunkte) je Kreis
neubau = (
    df_new.groupby("Kreis_kreisfreie_Stadt")["Anzahl Ladepunkte"]
    .sum().reset_index(name="neue_ladepunkte")
)
# Top5
top5 = neubau.nlargest(5, "neue_ladepunkte")
bot5 = neubau.nsmallest(5, "neue_ladepunkte")
# Kombiniere für Diagramm
chart_df = pd.concat([top5.assign(Rang="Top 5"), bot5.assign(Rang="Bottom 5")])
# Plot mit Plotly
fig = px.bar(
    chart_df,
    x="neue_ladepunkte",
    y="Kreis_kreisfreie_Stadt",
    color="Rang",
    orientation="h",
    labels={
        "neue_ladepunkte": "Anzahl neuer Ladepunkte",
        "Kreis_kreisfreie_Stadt": "",
        "Rang": "Kategorie"
    },
    title=f"Ladepunkte im Zeitraum seit {cutoff.date()}"
)
st.plotly_chart(fig, use_container_width=True)

# streamlit run chargingpoints_by_district.py
