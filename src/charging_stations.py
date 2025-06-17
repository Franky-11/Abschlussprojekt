import streamlit as st


col1,col2=st.columns([1,1])
with col1:
    st.header("")
    st.write("")

    st.title("Ladensäuleninfrastruktur :material/ev_station:")

with col2:
    st.image("images/charging-station-4636710_1920.jpg",use_container_width=True)


st.divider()