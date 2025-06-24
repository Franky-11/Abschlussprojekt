import streamlit as st

# Seitenoptionen
pages = {
    "Home": "home",
    "Fahrzeugmarkt":"cars",
    "Strombedarf": "strombedarf",
    "Strombedarf-Simulator": "strombedarf_simulator",
    "Stromerzeugung":"stromerzeugung",
    "Ladeinfrastruktur-Map": "ladeinfrastruktur_map",
    "Ladesäuleninfrastruktur":"charging_stations",
    "Netz-Stress-Test": "netz_stress_test",
    "Akzeptanz-Radar": "akzeptanz_radar",
    "Fazit": "fazit"
}

st.sidebar.title("🔀 Navigation")
selection = st.sidebar.selectbox("Wähle eine Seite", list(pages.keys()))

# Dynamisches Laden der Seite
page_module = __import__(f"{pages[selection]}")
page_module.run()
