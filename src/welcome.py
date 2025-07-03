import streamlit as st
from watermarks import set_watermark


def run():
    set_watermark("images/watermark/chargingpoints_pic.png")
    st.title("Willkommen")

    st.header("Realitätscheck E-Mobilität – Ein datengetriebener Blick auf Deutschlands Weg zur Elektromobilität")

