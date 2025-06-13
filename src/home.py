import streamlit as st


st.set_page_config(layout="wide")


dashboard = st.Page("Dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)

intro = st.Page("intro.py", title="Projektbeschreibung", icon=":material/info:")

cars=st.Page("cars.py", title="Fahrzeugbestand", icon=":material/directions_car:")

charging_stations=st.Page("charging_stations.py", title="Ladensäuleninfrastruktur", icon=":material/electrical_services:")


pg = st.navigation(pages=[intro, cars])#,charging_stations])

#pg = st.navigation({"Projektbeschreibung": [intro],"Fahrzeugbestand":[cars],"Strombedarf & Stromerzeugung": [dashboard]})


pg.run()


