import streamlit as st
import plotly.graph_objects as go
from watermarks import set_watermark


def run():
    set_watermark("images/watermark/chargingpoints_pic.png")
    #set_watermark("src/images/watermark/chargingpoints_pic.png")
  
    st.title("📘 Fazit – Deutschlands E-Mobilitätswende im Realitätscheck")

    st.markdown("## ⚡ Zusammenfassung & Ausblick")
    st.markdown("""
    Die zentralen Ergebnisse unseres Projekts zeigen:  
    - **machbar**: Erneuerbare Energien können diesen Bedarf decken.
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
    - Zielsetzung Bundesregierung: **1. Mio** Ladepunkte bis 2030 = unrealistisch & unnötig
    - 15 Mio BEV´s bis 2030: 2025 = 1,68 Mio Fahrzeuge -> das wären 2,7 Mio neue BEV´s/Jahr
    - **Verteilnetze** müssen jedoch verstärkt & gesteuert werden.
    - **Gesteuertes Laden**, dynamische Tarife & **bidirektionales Laden** (V2G) können Engpässe entschärfen
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
    
    st.title("📡 Akzeptanz-Radar")
    st.markdown("""
        Die Akzeptanz der Elektromobilität hängt stark von emotionalen, technischen und infrastrukturellen Faktoren ab. 
        In dieser Ansicht kannst du typische Einflussfaktoren aktivieren, die die Zustimmung der Bevölkerung erhöhen oder senken – simulativ oder auf Basis realer Umfragen.
        """)

    st.subheader("🧠 Einflussfaktoren auf die Akzeptanz")

    basis_akzeptanz = 68
    akzeptanz_delta = 0

    faktoren = [
        ("🔌 Unzureichende Ladeinfrastruktur", -3,
         "Trotz politischer Zielvorgaben ist der Ausbau öffentlicher Ladepunkte regional stark unterschiedlich. Besonders in ländlichen Gebieten fehlt es an verlässlicher Ladeinfrastruktur, was den Alltag mit einem E-Fahrzeug erschwert."),
        ("⛽ Reichweitenangst", -3,
         "Viele potenzielle Käufer:innen zweifeln, ob sie mit einem E-Auto ihre täglichen und insbesondere spontanen oder langen Strecken zuverlässig bewältigen können. Die subjektiv empfundene Unsicherheit beeinflusst die Kaufentscheidung negativ."),
        ("💰 Hohe Anschaffungskosten", -3,
         "E-Autos sind in der Regel teurer in der Anschaffung als vergleichbare Verbrenner – auch trotz staatlicher Förderungen. Für einkommensschwächere Haushalte stellt dies eine reale Hürde dar."),
        ("⚡ Angst vor Netzüberlastung", -3,
         "In der öffentlichen Debatte steht die Sorge, dass das Stromnetz durch massenhaftes gleichzeitiges Laden kollabieren könnte. Diese Unsicherheit wird teils von Medien befeuert und wirkt abschreckend."),
        ("🏘️ Kein Zugang zu Heimladung", -3,
         "Ein Großteil der Bevölkerung in Städten wohnt zur Miete und hat weder eine eigene Garage noch einen Stellplatz mit Lademöglichkeit. Ohne einfache Ladelösung zu Hause fehlt der Komfortvorteil."),
        ("🚘 Fehlende Fahrzeugvielfalt", -2,
         "Das Angebot an E-Fahrzeugen hat sich verbessert, doch viele Segmente wie Kombis oder Nutzfahrzeuge sind weiterhin unterrepräsentiert. Das erschwert den Umstieg für bestimmte Nutzergruppen."),
        ("🧓 Altersstruktur & Technikskepsis", -2,
         "Gerade ältere Zielgruppen stehen der Elektromobilität mit Vorbehalten gegenüber. Oft fehlt Vertrauen in neue Technologien oder es besteht eine enge Bindung an gewohnte Fahrweisen."),
        ("🌍 Hohes Klimabewusstsein", +5,
         "Wer sich aktiv mit Umwelt- und Klimaschutz auseinandersetzt, bewertet emissionsfreie Mobilität tendenziell positiv. Klimabewusste Einstellungen fördern die Akzeptanz deutlich."),
        ("🎯 Kaufprämien & Förderung", +5,
         "Staatliche Zuschüsse, steuerliche Vorteile und Förderprogramme senken die Einstiegshürde für viele Haushalte – und signalisieren politische Rückendeckung."),
        ("🗞️ Negative Berichterstattung", -3,
         "Medien, die Schlagzeilen über brennende Akkus oder seltene Rohstoffe in den Vordergrund stellen, erzeugen Angst und Zweifel – oft ohne differenzierte Einordnung.")
    ]

    st.markdown("### 💡 Einfluss auswählen")

    for i, (label, impact, tooltip) in enumerate(faktoren):
        cols = st.columns([0.9, 0.1])
        with cols[0]:
            selected = st.checkbox(label, key=f"cb_{i}")
        with cols[1]:
            st.markdown(f"<span title='{tooltip}'>ℹ️</span>", unsafe_allow_html=True)
        if selected:
            akzeptanz_delta += impact

    akzeptanz = max(0, min(100, basis_akzeptanz + akzeptanz_delta))

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=akzeptanz,
        title={"text": "Akzeptanz der Elektromobilität"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 50], "color": "red"},
                {"range": [50, 75], "color": "orange"},
                {"range": [75, 100], "color": "green"}
            ]
        }
    ))

    st.plotly_chart(fig, use_container_width=True)

    
    st.success("✅ **Deutschlands Energielandschaft mit vollelektrischen Fahrzeugen ist machbar – wenn Energiewende, Netzausbau & gesellschaftlicher Wandel Hand in Hand gehen.**")


