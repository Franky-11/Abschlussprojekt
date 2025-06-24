import streamlit as st

import home
import cars
import strombedarf
import StrombedarfSimulator
import strombedarf_simulator
import ladeinfrastruktur_map
import netz_stress_test
import akzeptanz_radar
import fazit


# Seitenoptionen
pages = {
    "Home":home,
    "Fahrzeugmarkt":cars,
    "Strombedarf":strombedarf,
    "StrombedarfSimulator":StrombedarfSimulator,
    "Strombedarf-Simulator": strombedarf_simulator,
    "Stromerzeugung":stromerzeugung,
    "Ladeinfrastruktur-Map": ladeinfrastruktur_map,
    "Netz-Stress-Test": netz_stress_test,
    "Akzeptanz-Radar": akzeptanz_radar,
    "Fazit": fazit
}

st.sidebar.title("🔀 Navigation")
selection = st.sidebar.selectbox("Wähle eine Seite", list(pages.keys()))

# Dynamisches Laden der Seite
# page_module = __import__(f"{pages[selection]}")
pages[selection].run()



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
