import streamlit as st



st.title("Deutschlands E-Auto-Wende im Daten-Audit")


st.image("images/co2-4767388_1920.jpg",width=400,use_container_width=True)


st.divider()
col1,col2=st.columns([1.7,1])

with col1:
    st.header("Hintergrund & Motivation")
    st.subheader("Das geplante Aus für Verbrenner ab 2035")
    st.markdown("""
    Die Europäische Union hat das Ziel festgelegt, ab **2035 nur noch emissionsfreie Neuwagen** zuzulassen.    
    Doch was steckt dahinter und welche Auswirkungen hat das?
    """)
with col2:
    st.write("")  # Eine leere Zeile
    st.write("")  # Eine leere Zeile
    st.write("")  # Eine leere Zeile
    st.image("images/electric-car-2545290_1280.png", width=400, use_container_width=True)

tab1,tab2,tab3=st.tabs(["Warum das Ganze?","Was ist betroffen?","Aktueller Diskussionsstand"])

with tab1:
    st.markdown("""
        **Warum das Ganze?**
        * :material/eco: **Klimaschutz:** Primäres Ziel ist die massive Reduzierung der Treibhausgasemissionen im Verkehrssektor, um die EU-Klimaziele bis 2030 und die Klimaneutralität bis 2050 zu erreichen.
        * :material/air: **Verbesserung der Luftqualität:** Reduzierung von lokalen Schadstoffen (Feinstaub, Stickoxide), besonders in städtischen Gebieten.
        * :material/lightbulb: **Förderung von Innovation:** Anreiz für die Automobilindustrie, verstärkt in Elektromobilität und grüne Technologien zu investieren.
        * :material/rule: **Planungssicherheit:** Schaffung klarer Rahmenbedingungen für Hersteller und Verbraucher.
        """)

with tab2:
    st.markdown("""
    **Was ist betroffen?**
    * :material/new_releases: **Neue Pkw & leichte Nutzfahrzeuge:** Ab 2035 dürfen in der EU keine **neuen** Fahrzeuge mehr zugelassen werden, die ausschließlich mit fossilem Benzin oder Diesel betrieben werden.
    * :material/fuel: **Ausnahme für E-Fuels:** Fahrzeuge, die nachweislich ausschließlich mit CO2-neutralen synthetischen Kraftstoffen (E-Fuels) betrieben werden können, sollen weiterhin neu zugelassen werden dürfen.
    * :material/autorenew: **Bestandsfahrzeuge:** Alle bis 2034 zugelassenen Verbrenner-Fahrzeuge dürfen weiterhin uneingeschränkt gefahren und gehandelt werden. Es gibt kein Verbot für den Betrieb bestehender Fahrzeuge!
    """)

with tab3:
    st.markdown("""
    **Aktueller Diskussionsstand**
    * Die Regelung wird voraussichtlich 2026 überprüft. Aktuell gibt es Diskussionen über eine mögliche Aufweichung oder stärkere Berücksichtigung von E-Fuels im Rahmen der "Technologieoffenheit".
    """)



st.divider()

st.markdown(" ### Projektziele")
st.markdown("""
    * **Fahrzeugbestand und Energieverbrauch**
    * **Ladeinfrastruktur** 
    * **Emissionsreduktion**
    """)

st.divider()
with st.expander("Mehr über das Projektteam",icon=":material/group:"):
    st.write("Diese App wurde entwickelt von:")
    st.markdown("""
    * **Frank Schulnies**: App-Design, Fahrzeugbestand
    * **Phillip Schauer**: Ladensäuleninfrastrukutur
    * **Thomas Baur**: Emissionen
    """)



with st.expander("Quellen & Datensätze", icon=":material/library_books:"):
    st.markdown("""
    **Verwendete Datensätze:**
    * **[Name des Datensatzes 1]**: Bezugsquelle: [Link zum Datensatz, falls öffentlich verfügbar], Lizenz: [Lizenzinformationen, z.B. CC BY 4.0]
        * Kurzbeschreibung: [Was beinhaltet dieser Datensatz?]
    * **[Name des Datensatzes 2]**: Bezugsquelle: [Link], Lizenz: [Lizenz]
        * Kurzbeschreibung: [Was beinhaltet dieser Datensatz?]

    **Wissenschaftliche Quellen / Literatur:**
    * [Autor(en), Jahr], *Titel des Artikels/Buches*, [Journal/Verlag]. [Link zur Quelle, falls verfügbar]
    * [Autor(en), Jahr], *Titel des Artikels/Buches*, [Journal/Verlag]. [Link zur Quelle, falls verfügbar]

    **Bilder:**
    * https://pixabay.com/de/illustrations/co2-abgase-verkehrszeichen-auto-4767388/
    * https://pixabay.com/de/vectors/elektroauto-ladestation-e-auto-2545290/
    * 
    * 
    * 
    * 
    """)
