import streamlit as st

def run():
    st.title("🚗 Deutschlands E-Mobilitätswende – Ein datenbasierter Realitätscheck")

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
    - Rückblick auf Entwicklungstrends (bis 2020)  
    - Status Quo: Stand 2024  
    - Etappen-Ziele bis 2025  
    - Ausbaupläne & Zielbild 2030  
    - Prognosen bis 2035 und darüber hinaus
    """)

    st.markdown("### 🔍 Analysefokus")
    st.markdown("""
    - Zusätzlicher Strombedarf durch BEVs  
    - Belastbarkeit und Modernisierung des Stromnetzes  
    - Flächenverfügbarkeit & Ausbaupotenzial Erneuerbarer  
    - Wechselwirkungen zwischen Sektoren (Sektorkopplung)  
    - Akzeptanz, Gesellschaft & Markt
    """)

    st.success("Nutze die Navigation links, um durch die einzelnen Kapitel und Visualisierungen zu navigieren.")
