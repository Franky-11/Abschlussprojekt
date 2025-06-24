import streamlit as st

def run():
    st.title("📘 Fazit – Deutschlands E-Mobilitätswende im Realitätscheck")

    st.markdown("## ⚡ Zusammenfassung & Ausblick")
    st.markdown("""
    Die vollständige Elektrifizierung aller Straßenfahrzeuge in Deutschland würde den Strombedarf um ca. **150–180 TWh** pro Jahr erhöhen – was **25–30 %** des heutigen Stromverbrauchs entspricht.  
    Die zentralen Ergebnisse unseres Projekts zeigen:  
    - Technisch **machbar**: Erneuerbare Energien können diesen Bedarf decken.
    - Netzseitig **herausfordernd**: Lokale Netze brauchen **Modernisierung & Lastmanagement**.
    - Gesellschaftlich **kritisch**: **Akzeptanz**, Transparenz und soziale Teilhabe sind entscheidend.

    --- 
    """)

    st.markdown("### 🌐 1. Technische Machbarkeit")
    st.markdown("""
    - Mit dem geplanten Ausbau von Wind- und Solarenergie könnte Deutschland bis **2030 ca. 550–600 TWh** erneuerbaren Strom erzeugen.
    - Der Strommehrbedarf durch E-Mobilität ist **im Rahmen dieser Ausbauziele** enthalten.
    - **Flächenpotenzial vorhanden**: <3 % der Landesfläche für Wind & PV genügen.
    """)

    st.markdown("### 🔌 2. Netzinfrastruktur & Laststeuerung")
    st.markdown("""
    - Das **Übertragungsnetz** ist heute schon ausreichend dimensioniert.
    - **Verteilnetze** müssen jedoch verstärkt & gesteuert werden.
    - **Gesteuertes Laden**, dynamische Tarife & **bidirektionales Laden** (V2G) können Engpässe entschärfen.
    """)

    st.markdown("### 🧠 3. Systemische Kopplung & smarte Energiezukunft")
    st.markdown("""
    - Elektromobilität ist **Teil eines größeren Stromverbrauchertrends** (Wärme, Industrie, etc.).
    - E-Autos können perspektivisch als **Stromspeicher** agieren.
    - Die Sektorenkopplung muss **strategisch geplant** und umgesetzt werden.
    """)

    st.markdown("### 🤝 4. Gesellschaftliche & politische Erfolgsfaktoren")
    st.markdown("""
    - **Akzeptanz** in Bevölkerung & Wirtschaft ist Schlüssel für Umsetzung.
    - **Genehmigungsprozesse beschleunigen**, Kommunen & Bürger*innen beteiligen.
    - **Zielbild 2030** erreichbar – mit ausreichender **politischer Konsequenz** und **gesellschaftlichem Schulterschluss**.
    """)

    st.success("✅ Deutschlands Energielandschaft mit vollelektrischen Fahrzeugen ist machbar – wenn Energiewende, Netzausbau & gesellschaftlicher Wandel Hand in Hand gehen.")


# Einfacher Taschenrechner am Ende der Seite
def simple_calculator():
    st.markdown("---")
    st.markdown("## 🧮 Einfacher Taschenrechner")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        num1 = st.number_input("Zahl 1", value=0.0)
    with col2:
        operation = st.selectbox("Operation", ["+", "-", "*", "/"])
    with col3:
        num2 = st.number_input("Zahl 2", value=0.0)

    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "/":
        result = num1 / num2 if num2 != 0 else "Division durch 0 nicht erlaubt"
    else:
        result = "Ungültige Operation"

    st.markdown(f"**Ergebnis:** {result}")

simple_calculator()
