import streamlit as st


st.set_page_config(layout="wide")


dashboard = st.Page("Dashboard.py", title="Dashboard", icon=":material/dashboard:", default=True)

daten = st.Page("Daten.py", title="Data", icon=":material/database:")

pg = st.navigation( { "Daten": [daten],"Reports": [dashboard] })

pg.run()


