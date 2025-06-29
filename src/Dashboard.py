import streamlit as st

import home
import cars
import strombedarf
#import StrombedarfSimulator
#import strombedarf_simulator
import stromerzeugung

import netz_stress_test
import akzeptanz_radar
import fazit
import chargingpoints_by_district
import number_of_chargingstations
import optimierung_lp_dist


# Seitenoptionen
st.set_page_config(layout="wide")


pages = {
    "Home":home,
    "Fahrzeugmarkt":cars,
    "Strombedarf":strombedarf,
    #"StrombedarfSimulator":StrombedarfSimulator,
    #"Strombedarf-Simulator": strombedarf_simulator,
    "Stromerzeugung":stromerzeugung,
    "Ladeinfrastruktur-Map": chargingpoints_by_district,
    "Entwicklung der Ladesäulen":number_of_chargingstations,
    "Optimierung Ladepunktverteilung":optimierung_lp_dist,
    "Netz-Stress-Test": netz_stress_test,
    "Akzeptanz-Radar": akzeptanz_radar,
    "Fazit": fazit
}

# --- Ergänzung: Fallback, falls ein Modul keine run()-Funktion hat
for _name, _mod in pages.items():
    if not hasattr(_mod, "run"):
        if hasattr(_mod, "st_display"):
            # st_display als Ersatz für run verwenden
            _mod.run = _mod.st_display
        else:
            # Platzhalter, damit das Dashboard nicht abstürzt
            def _placeholder(name=_name):
                st.error(f"Die Seite '{name}' hat keine ausführbare Funktion.")
            _mod.run = _placeholder

st.sidebar.title("🔀 Navigation")
selection = st.sidebar.selectbox("Wähle eine Seite", list(pages.keys()))

# Dynamisches Laden der Seite
# page_module = __import__(f"{pages[selection]}")
pages[selection].run()


# --- Ergänzung: SMARD-Daten nur für die Stromerzeugung‑Seite anzeigen
if selection == "Stromerzeugung" and hasattr(stromerzeugung, "get_smard_data"):
    latest_ts, need_df, gen_df = stromerzeugung.get_smard_data()
    if latest_ts is None:
        st.error("Fehler beim Laden der SMARD-Daten.")
    else:
        st.subheader("🟢 Stromverbrauch und -erzeugung laut SMARD")
        st.markdown(f"**Zeitstempel:** {latest_ts}")
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Strombedarf (Verbrauch):**")
            st.dataframe(need_df)
        with col2:
            st.markdown("**Stromerzeugung (gesamt):**")
            st.dataframe(gen_df)



# Fabians Beispiel
#pages = {
#    "1. Streamlit"   : tutorial_page,
#    "2. Widgets"     : widgets_page,
#    "3. Daten"       : daten_page,
#    "4. Karte"       : map_page,
#    "5. Gastgeber"   : hosts_page,
#    "6. Bewertungen" : reviews_page,
#    "7. Fazit"       : fazit_page
#}

# Erstelle eine Seitenleiste für die Navigation im Projekt
#st.sidebar.title("Navigation")
#select = st.sidebar.radio("Gehe zu:", list(pages.keys()))

# Starte die ausgewählte Seite
# pages[select].app()
