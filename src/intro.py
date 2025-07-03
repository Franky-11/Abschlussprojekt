import streamlit as st
from watermarks import set_watermark


def run():


    set_watermark("images/watermark/chargingpoints_pic.png")
    st.title("Realitätscheck E-Mobilität – Ein datengetriebener Blick auf Deutschlands Weg zur Elektromobilität")


    st.markdown("### 🧭 Einleitung & Fragestellung")
    st.markdown("""
    Die Mobilitätswende gilt als entscheidender Baustein auf dem Weg zur Klimaneutralität. 
    Doch sind die politischen Zielsetzungen zur vollständigen Elektrifizierung des Straßenverkehrs – etwa 15 Millionen E-Fahrzeuge bis 2030 – unter den heutigen Rahmenbedingungen überhaupt erreichbar?

    In diesem Projekt analysieren wir die zentralen Einflussfaktoren mithilfe aktueller Datenquellen und interaktiver Visualisierungen. 

    **Leitfrage:**  
    *Sind die Ziele zur E-Mobilität realistisch erreichbar – und was müsste geschehen, damit sie Wirklichkeit werden können?*

    Der Realitätscheck umfasst neben technischen und energetischen Aspekten auch gesellschaftliche, infrastrukturelle und wirtschaftliche Einflussgrößen.
    """)

    st.markdown("### 🛠️ Projektverlauf")
    st.markdown("""
    - **Themenfindung** & Zieldefinition im Team  
    - Auswahl technischer & organisatorischer Tools: `GitHub`, `Streamlit`, `Scrum`  
    - Iterative Entwicklung mit agilen Etappen  
    - Visualisierung & Validierung mit Stakeholder-Fokus  
    - Abgeleitetes **Gesamtfazit** mit klaren Empfehlungen
    - Integration interaktiver Dashboards zur Ableitung datenbasierter Handlungsoptionen
    """)

    st.markdown("Unsere Analyse betrachtet sowohl historische Entwicklungen als auch aktuelle und zukünftige Szenarien.")
    st.markdown("### 📅 Untersuchungszeiträume")
    st.markdown("""
    - Rückblick auf Entwicklungstrends 
    - Status Quo
    - Prognosen bis 2035 und darüber hinaus
    """)

    st.markdown("### 🔍 Analysefokus")
    st.markdown("""
    Unser Analysemodell berücksichtigt sowohl technische als auch gesellschaftliche Dimensionen der Elektromobilität:

    - Stromerzeugung & Versorgungsinfrastruktur  
    - Zusätzlicher Strombedarf durch vollelektrische Pkw  
    - Entwicklung des Fahrzeugmarkts  
    - Ladeinfrastruktur & Netzausbau  
    - Gesellschaftliche Akzeptanz und wirtschaftliche Rahmenbedingungen
    """)

    st.success("Nutze die Navigation links, um durch die einzelnen Kapitel und Visualisierungen zu navigieren.")



  # Belastbarkeit und Modernisierung des Stromnetzes
# - Flächenverfügbarkeit & Ausbaupotenzial
   #Erneuerbarer
#- Wechselwirkungen zwischen Sektoren(Sektorkopplung)
