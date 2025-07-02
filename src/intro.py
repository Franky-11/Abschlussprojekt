import streamlit as st
import streamlit as st
from watermarks import set_watermark
set_watermark("images/watermark/chargingpoints_pic.png")

def run():
    st.title("Realitätscheck E-Mobilität – Ein datengetriebener Blick auf Deutschlands Weg zur Elektromobilität")

    st.markdown("### 🧭 Einleitung & Fragestellung")
    st.markdown("""
    Die Mobilitätswende in Deutschland ist eine der zentralen Säulen der Energietransformation. 
    Unser Projekt untersucht, ob die von der Bundesregierung formulierten Ziele zur Elektromobilität realistisch erreichbar sind – und unter welchen Voraussetzungen.

    **Leitfrage**:  
    *„Unsere Bundesregierung hat Ziele zur E-Mobilität gesetzlich verankert.“ Doch sind diese Ziele realistisch und erreichbar?*

    Neben klassischen Parametern wie Stromerzeugung und Fahrzeugentwicklung betrachten wir auch gesellschaftliche, infrastrukturelle und technologische Faktoren.
    """)

    st.markdown("### 🛠️ Projektverlauf")
    st.markdown("""
    - **Themenfindung** & Zieldefinition im Team  
    - Auswahl technischer & organisatorischer Tools: `GitHub`, `Streamlit`, `Scrum`  
    - Iterative Entwicklung mit agilen Etappen  
    - Visualisierung & Validierung mit Stakeholder-Fokus  
    - Abgeleitetes **Gesamtfazit** mit klaren Empfehlungen
    """)

    st.markdown("### 📅 Untersuchungszeiträume")
    st.markdown("""
    - Rückblick auf Entwicklungstrends 
    - Status Quo
    - Prognosen bis 2035 und darüber hinaus
    """)

    st.markdown("### 🔍 Analysefokus")
    st.markdown("""
    - Fahrzeugmarkt
    - Zusätzlicher Strombedarf durch BEVs  
    - Ladeinfrastruktur
    - Stromerzeugung
    - Akzeptanz, Gesellschaft & Markt
    """)

    st.success("Nutze die Navigation links, um durch die einzelnen Kapitel und Visualisierungen zu navigieren.")

  # Belastbarkeit und Modernisierung des Stromnetzes
# - Flächenverfügbarkeit & Ausbaupotenzial
   #Erneuerbarer
#- Wechselwirkungen zwischen Sektoren(Sektorkopplung)
