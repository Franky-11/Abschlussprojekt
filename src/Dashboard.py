import streamlit as st
import time

st.header("Dashboard")

row1=st.columns(2)
chart1=row1[0].container(border=True)
chart2=row1[1].container(border=True)
row2=st.columns(2)
chart3=row2[0].container(border=True)
chart4=row2[1].container(border=True)

placeholder=st.empty() # Platzhalter
#st.container()) inside st.empty
with chart1:
    st.markdown("***Chart 1***")


with chart2:
    st.markdown("***Chart 2***")


with chart3:
    st.markdown("***Chart 3***")

with chart4:
    st.markdown("***Chart 4***")