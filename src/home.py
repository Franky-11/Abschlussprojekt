import streamlit as st
import importlib

st.set_page_config(page_title="E-Mobilität", layout="wide")

# ───────────────────────── Seiten-Register ─────────────────────────
# Hinweis: Alle Seiten-Module müssen eine run() Funktion enthalten
pages = {
    "Willkommen": "welcome",                 # Startseite
    "Intro": "intro",
    "Scrum": "scrum",
    "Stromerzeugung": "energy_production",
    "Energie-Lieferanten": "energy_suppliers",
    "Fahrzeugmarkt": "cars",
    "Stromverbrauch & -bedarf": "energy_consumption",
    "Ladeinfrastruktur": "chargingpoints_by_district",
    "Ladepunktentwicklung": "number_of_chargingstations",
    "Ladepunktverteilung": "charging_point_opt",
    "Fazit": "conclusion",
}


# ───────────────────────── Sidebar ─────────────────────────
st.sidebar.title("🔀 Navigation")
selection = st.sidebar.selectbox("Wähle eine Seite", list(pages.keys()))
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

    st.error(f"Fehler beim Laden von '{module_name}': {e}")
