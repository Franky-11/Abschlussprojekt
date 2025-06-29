import streamlit as st
import pandas as pd
import folium
from folium.map import Icon
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from folium import Element


@st.cache_data
def lade_und_bereinige_daten(pfad):
    df = pd.read_csv(pfad,
                     sep=';',
                     encoding='ISO-8859-1',
                     dtype=str)
    relevante_spalten = ["Breitengrad", "Längengrad", "Ort", "Straße", "Hausnummer", "Art der Ladeeinrichtung"]

    # Fehlende Werte entfernen
    df = df[relevante_spalten].dropna(subset=["Breitengrad", "Längengrad"])

    def ist_gueltig(val):
        val = str(val).replace('.', '')
        return val.isdigit()

    def format_breitengrad(val):
        val = str(val).replace('.', '')
        val = val.ljust(8, '0')[:8]
        return f"{val[:-6]}.{val[-6:]}"  # z.B. 51805270 → 51.805270

    def format_laengengrad(val):
        val = str(val).replace('.', '')
        if val.startswith("1"):
            val = val.ljust(8, '0')[:8]
        else:
            val = val.ljust(7, '0')[:7]
        return f"{val[:-6]}.{val[-6:]}"  # z.B. 10332870 → 10.332870

    df = df[df["Breitengrad"].apply(ist_gueltig)]
    df = df[df["Längengrad"].apply(ist_gueltig)]

    df["Breitengrad"] = df["Breitengrad"].apply(format_breitengrad).astype(float)
    df["Längengrad"] = df["Längengrad"].apply(format_laengengrad).astype(float)

    # Nur Koordinaten in Deutschland behalten
    df = df[
        df["Breitengrad"].between(47.0, 55.1) &
        df["Längengrad"].between(5.5, 15.5)
        ]

    return df

#Daten einlesen
df = lade_und_bereinige_daten("C:/Users/PC/Desktop/Abschlussprojekt/data/electric_vehicles/Ladesaeulenregister_BNetzA.csv")

print(f"Aktuell verbleibende Datensätze: {len(df)}")

# Ladearten-Filter
ladearten = df["Art der Ladeeinrichtung"].dropna().unique().tolist()
ladearten.sort()

auswahl = st.multiselect(
    "Art der Ladeeinrichtung auswählen:",
    options=ladearten,
    default=ladearten  # beide standardmäßig aktiv
)
df = df[df["Art der Ladeeinrichtung"].isin(auswahl)]

# Ortsfilter
ort_filter = st.text_input("Ortsname enthält (optional):").strip()
if ort_filter:
    df = df[df["Ort"].str.contains(ort_filter, case=False, na=False)]

# Markeranzahl begrenzen
MAX_MARKER = 88575
if len(df) > MAX_MARKER:
    df = df.sample(MAX_MARKER, random_state = 1)

st.write(f"Angezeigte Ladesäulen: {len(df)}")

# Karte erzeugen
with st.spinner("Karte wird geladen..."):
    m = folium.Map(location= [51.5000, 14.0000], zoom_start = 6, prefer_canvas=True)
    marker_cluster = MarkerCluster().add_to(m)

    farben = {
        "Normalladeeinrichtung": "blue",
        "Schnellladeeinrichtung": "red"
    }


    # Marker hinzufügen (hier: max. 10.000 für Performance)
    for _, row in df.iterrows():
        ladeart = row.get("Art der Ladeeinrichtung", "Unbekannt")
        farbe = farben.get(ladeart, "gray")

        popup_text = f"{row.get('Ort', '')}, {row.get('Straße', '')} {row.get('Hausnummer', '')}"
        folium.Marker(
            location=[row["Breitengrad"], row["Längengrad"]],
            popup=popup_text,
            icon = Icon(color=farbe, icon="bolt", prefix="fa")
        ).add_to(marker_cluster)

    legende_html = """
    <div style="
        position: fixed;
        bottom: 50px;
        right: 30px;
        z-index: 9999;
        background-color: rgba(30, 30, 30, 0.9);
        padding: 10px 15px;
        border: 2px solid #444;
        border-radius: 5px;
        box-shadow: 2px 2px 6px rgba(0,0,0,0.3);
        color: white;
        font-size: 14px;
    ">
        <strong style='color: white;'>Ladearten</strong><br>
        <i style='background: red; width: 10px; height: 10px; display: inline-block; margin-right: 5px;'></i>
        Schnellladeeinrichtung<br>
        <i style='background: blue; width: 10px; height: 10px; display: inline-block; margin-right: 5px;'></i>
        Normalladeeinrichtung
    </div>
    """

    m.get_root().html.add_child(Element(legende_html))

    st_folium(m, width=900, height=600)


# Zum Starten von Streamlit: streamlit run Ladesaeulenregister_Streamlit_Kartenvisualisierung.py