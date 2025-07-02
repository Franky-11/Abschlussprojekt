""""
if 'animation_active' not in st.session_state:
    st.session_state.animation_active = False

if 'animation_finished' not in st.session_state:
    st.session_state.animation_finished = False

if 'percent_checked' not in st.session_state:
    st.session_state.percent_checked = False
""""

""""
df = read_df_cars()
with tab1:
     with st.container(border=True,height=550):
        change=(df["cars_sum"].iloc[0]-df["cars_sum"].iloc[-1])/df["cars_sum"].iloc[-1]*100
        st.markdown(f"##### :material/trending_up: {change:.1f}%")
        fig1=plot_cars(df)
        st.plotly_chart(fig1)


with tab2:
    with st.container(border=True,height=550):
        col1,col2=st.columns([1,3])
        with col1:
            start_button_clicked=st.button("Start")
            status_placeholder = st.empty()
        with col2:
            st.checkbox("Anteil E-Car", key="percent_checked")
            st.checkbox("Events", key="annot_checked")
           # st.session_state.percent_checked=st.checkbox("Anteil E-Car",value=st.session_state.percent_checked, key="percent_checkbox")
           # st.session_state.annot_checked = st.checkbox("Events", value=st.session_state.annot_checked, key="events_checkbox")

        plot_placeholder = st.empty()

        if start_button_clicked:
            st.session_state.animation_active = True
            st.session_state.animation_finished = False

        if st.session_state.animation_active:
            for i in range(1, len(df)+1):
                df_filtered=df.iloc[-i::]
                growth_factor = (df_filtered["e_cars"].iloc[0] / df_filtered["e_cars"].iloc[-1])
                status_placeholder.markdown(f"##### :material/arrow_upward: {growth_factor:.0f}-fache")
                fig2 = plot_e_cars(df_filtered,False)
                plot_placeholder.plotly_chart(fig2)
                time.sleep(0.1)

            st.session_state.animation_active = False
            st.session_state.animation_finished = True
            st.rerun()

        if not st.session_state.animation_active:
            fig=None
            if st.session_state.percent_checked:
                fig=plot_e_cars_percent(df,False)
                if st.session_state.annot_checked:
                    fig=plot_e_cars_percent(df,True)

            elif st.session_state.annot_checked:
                fig=plot_e_cars(df,True)

            elif st.session_state.animation_finished:
                fig = plot_e_cars(df,False)
                growth_factor = (df["e_cars"].iloc[0] / df["e_cars"].iloc[-1])
                status_placeholder.markdown(f"##### :material/arrow_upward: {growth_factor:.0f}-fache")
            if fig is not None:
                plot_placeholder.plotly_chart(fig)

"""



import streamlit as st
from streamlit_folium import st_folium
import folium
from folium.map import Icon
from folium.plugins import MarkerCluster
from folium import Element

from charging_stations_functions import lade_und_bereinige_daten

st.header("Ladesäuleninfrastruktur")

pfad = "../data/electric_vehicles/Ladesaeulenregister_BNetzA.CSV"
df = lade_und_bereinige_daten(pfad)

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
    df = df.sample(MAX_MARKER, random_state=1)

st.write(f"Angezeigte Ladesäulen: {len(df)}")

# Karte erzeugen
with st.spinner("Karte wird geladen..."):
    m = folium.Map(location=[51.5000, 14.0000], zoom_start=6, prefer_canvas=True)
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
            icon=Icon(color=farbe, icon="bolt", prefix="fa")
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



### ---PLZ Visualisierung BEV (Frank)-------------------------------------------------------------------------------------#

if 'plz_fig' not in st.session_state:
    st.session_state.plz_fig = None

col1,col2=st.columns([4,2])

with col1:
    with st.container(border=True):

        eingabe_plz = st.text_input("Geben Sie eine PLZ ein, um dorthin zu zoomen:", max_chars=5,
                                    placeholder="z.B. 06846")

        if st.button("Karte anzeigen") or st.session_state.plz_fig is None or eingabe_plz:
            with st.spinner("Lade Geodaten..."):
                geo_json_plz = read_geojson_plz()
            with st.spinner("Lade und mergen der Fahrzeug- und Geodaten......"):
                df_geo = read_df_geo()
                bev_kreise = read_df_cars_for_plz_map()
            default_center = {"lat": 51.0, "lon": 10.0}
            default_zoom = 5
            center_map = default_center
            zoom_level = default_zoom

            if eingabe_plz:
                eingabe_plz_formatted = str(eingabe_plz).strip().zfill(5)
                plz_row = bev_kreise[bev_kreise['PLZ'] == eingabe_plz_formatted]
                if not plz_row.empty:
                    center_map["lat"] = plz_row["lat"].iloc[0]
                    center_map["lon"] = plz_row["lon"].iloc[0]
                    zoom_level = 10
                    st.success(f"Karte wird auf PLZ {eingabe_plz_formatted} zentriert.")
                else:
                    st.warning(f"PLZ {eingabe_plz_formatted} nicht in den Daten gefunden. Zeige Gesamtkarte.")

            with st.spinner("Lade Karte..."):
                st.session_state.plz_fig=plot_car_plz_map(bev_kreise,zoom_level,center_map,geo_json_plz)
                st.plotly_chart(st.session_state.plz_fig)



with col2:
    df_cars_for_map = read_df_cars_for_map()
    land_max, anteil_max = df_cars_for_map.loc[df_cars_for_map['Anteil_BEV'].idxmax()][["Bundesland", "Anteil_BEV"]]
    land_min, anteil_min = df_cars_for_map.loc[df_cars_for_map['Anteil_BEV'].idxmin()][["Bundesland", "Anteil_BEV"]]

    st.markdown(":material/monitoring: **Key facts**")
    st.metric(label="Höchster Anteil BEV", value=f"{land_max} | {round(anteil_max,1)}%")
    st.metric(label="Niedrigster Anteil BEV", value=f"{land_min} | {round(anteil_min,1)}%")


    #st.metric(label="Höchster Anteil BEV", value=f"{land_max} ({anteil_max}%)")


'-------------# BEV au PLZ Ebene----------------'
if 'plz_fig' not in st.session_state:
    st.session_state.plz_fig = None

col1, col2 = st.columns([4, 2])

with col1:
    with st.container(border=True):

        eingabe_plz = st.text_input("Geben Sie eine PLZ ein, um dorthin zu zoomen:", max_chars=5,
                                    placeholder="z.B. 06846")

        if st.button("Karte anzeigen") or st.session_state.plz_fig is None or eingabe_plz:
            with st.spinner("Lade Geodaten..."):
                geo_json_plz = read_geojson_plz()
            with st.spinner("Lade und mergen der Fahrzeug- und Geodaten......"):
                df_geo = read_df_geo()
                bev_kreise = read_df_cars_for_plz_map()
            default_center = {"lat": 51.0, "lon": 10.0}
            default_zoom = 5
            center_map = default_center
            zoom_level = default_zoom

            if eingabe_plz:
                eingabe_plz_formatted = str(eingabe_plz).strip().zfill(5)
                plz_row = bev_kreise[bev_kreise['PLZ'] == eingabe_plz_formatted]
                if not plz_row.empty:
                    center_map["lat"] = plz_row["lat"].iloc[0]
                    center_map["lon"] = plz_row["lon"].iloc[0]
                    zoom_level = 10
                    st.success(f"Karte wird auf PLZ {eingabe_plz_formatted} zentriert.")
                else:
                    st.warning(f"PLZ {eingabe_plz_formatted} nicht in den Daten gefunden. Zeige Gesamtkarte.")

            with st.spinner("Lade Karte..."):
                st.session_state.plz_fig = plot_car_plz_map(bev_kreise, zoom_level, center_map, geo_json_plz)
                st.plotly_chart(st.session_state.plz_fig)




#---------------------

# ───────────────────────── Dynamisches Laden ─────────────────────────
try:
    _mod = importlib.import_module(module_name)
    if hasattr(_mod, "run") and callable(_mod.run):
        _mod.run()
    else:
        raise AttributeError(
            f"Modul '{module_name}' enthält keine aufrufbare run()-Funktion"
        )

# ───────────────────────── Fallback: statische Startseite ─────────────────────────
except (ModuleNotFoundError, AttributeError):
    if selection == "Willkommen":
        st.markdown("### 🔍 Analysefokus")
        st.markdown(
            """
- Fahrzeugmarkt  
- Zusätzlicher Strombedarf durch BEVs  
- Ladeinfrastruktur  
- Stromerzeugung  
- Akzeptanz, Gesellschaft & Markt
"""
        )

        st.success(
            "Nutze die Navigation links, um durch die einzelnen Kapitel und Visualisierungen zu navigieren."
        )

        # ---------- Projektteam ----------
        with st.expander("Projektteam"):
            st.markdown(
                """
Dieses Projekt wurde im Rahmen unserer Data-Science-Weiterbildung erstellt.  
<br>
Data Science Institute by Fabian Rappert / DSI Education GmbH, Berlin  
<https://data-science-institute.de>

**Projektteam & Fokus**  
* **Philipp Schauer** – Ladeinfrastruktur  
* **Thomas Baur** – Projektmanagement, Stromerzeugung  
* **Frank Schulnies** – Fahrzeugmarkt  

Unser Ziel war es, ein nützliches und intuitives Tool zu entwickeln, das einen Beitrag zur Diskussion um die Zukunft der E-Mobilität leistet.
"""
            )
    else:
        st.error(f"Modul '{module_name}' konnte nicht geladen werden.")

# ───────────────────────── Unerwartete Fehler ─────────────────────────
except Exception as e:
    st.error(f"Fehler beim Laden von '{module_name}': {e}")






