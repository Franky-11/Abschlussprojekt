import streamlit as st


st.set_page_config(layout="wide")


#dashboard = st.Page("Dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)

intro = st.Page("intro.py", title="Projektbeschreibung", icon=":material/info:")

cars=st.Page("cars.py", title="Fahrzeugbestand", icon=":material/directions_car:")

strombedarf=st.Page("strombedarf.py", title="Strombedarf", icon=":material/electric_bolt:")

stromerzeugung=st.Page("stromerzeugung.py", title="Stromerzeugung", icon=":material/charging_station:")

fazit=st.Page("fazit.py", title="Fazit", icon=":material/fact_check:")


charging_stations=st.Page("charging_stations.py", title="Ladensäuleninfrastruktur", icon=":material/ev_station:")


pg = st.navigation(pages=[intro, cars, strombedarf,charging_stations, stromerzeugung, fazit])

#pg = st.navigation({"Projektbeschreibung": [intro],"Fahrzeugbestand":[cars],"Strombedarf & Stromerzeugung": [dashboard]})


pg.run()


