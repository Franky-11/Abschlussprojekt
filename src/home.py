import streamlit as st
import importlib

st.set_page_config(page_title="Dashboard", layout="wide")

# ───────────────────────── Seiten-Register ─────────────────────────
# Hinweis: Alle Seiten-Module müssen eine run() Funktion enthalten
pages = {
    "Willkommen": "welcome",                 # Startseite
    "Intro": "intro",
    # Scrum-Dashboard mit Burndown-Chart, Timeline und Meetingdaten
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
