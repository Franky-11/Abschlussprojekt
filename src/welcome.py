import streamlit as st
from watermarks import set_watermark


def run():
    set_watermark("images/watermark/chargingpoints_pic.png")
    st.title("Willkommen")
