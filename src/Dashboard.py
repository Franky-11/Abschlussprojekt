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
