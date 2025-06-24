
import streamlit as st


def run():
    col1,col2=st.columns([1,1])
    with col1:
        st.header("")
        st.write("")

        st.title("Stromerzeugung :material/charging_station:")

    with col2:
        st.image("images/power-lines-1809237_1920.jpg",use_container_width=True)


    st.divider()