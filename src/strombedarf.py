import streamlit as st


col1,col2=st.columns([1,1])
with col1:
    st.header("")
    st.write("")

    st.title("Strombedarf:material/electric_bolt:")

with col2:
    st.image("images/electricity-2595842_1280.jpg",use_container_width=True)


st.divider()

# Berechnung Strombedarf

# Die Berechnungen stützen sich auf Annahmen zum Fahrzeugbestand, zur Fahrleistung, zum spezifischen Energieverbrauch und zur Entwicklung der Ladeinfrastruktur.

# Jährliche Fahrleistung:
#  Der Energiebedarf wird auf Basis der voraussichtlichen jährlichen Fahrleistungen
#  der E-Fahrzeuge berechnet. Die Studie zur Ladeinfrastruktur geht beispielsweise von etwa 12.000 Kilometern pro Elektrofahrzeug pro Jahr aus

#  Energieverbrauch pro 100 km ist ein entscheidender Parameter.Für E - Pkw wird 15.8 kWh pro 100 km im Durchschnitt angenommen

# Bruttostromverbrauch in Dt. vergleich
