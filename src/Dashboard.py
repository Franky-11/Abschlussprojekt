
import streamlit as st
import importlib

st.set_page_config(page_title="Dashboard", layout="wide")

# Seitenoptionen
pages = {
    "Home": "home",
    "Fahrzeugmarkt": "cars",
    "Strombedarf": "strombedarf",
    "Strombedarf-Simulator": "strombedarf_simulator",
    "Stromerzeugung": "stromerzeugung",
    "Ladeinfrastruktur-Map": "ladeinfrastruktur_map",
    "Netz-Stress-Test": "netz_stress_test",
    "Akzeptanz-Radar": "akzeptanz_radar",
    "SMARD CSV Daten": "smard_csv_daten",
    "Fazit": "fazit"
}

st.sidebar.title("🔀 Navigation")
selection = st.sidebar.selectbox("Wähle eine Seite", list(pages.keys()))

# Dynamisches Laden und Ausführen der Seite
module_name = pages[selection]
try:
    _mod = importlib.import_module(module_name)
    if hasattr(_mod, "run") and callable(_mod.run):
        _mod.run()
    else:
        st.error(f"Modul '{module_name}' enthält keine aufrufbare 'run()'-Funktion.")
except ModuleNotFoundError as e:
    st.error(f"Modul nicht gefunden: {e}")
except Exception as e:
    st.error(f"Fehler beim Laden des Moduls '{module_name}': {e}")
