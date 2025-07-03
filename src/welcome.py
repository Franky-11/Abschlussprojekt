import streamlit as st
from watermarks import set_watermark
import base64


def run():
    set_watermark("images/watermark/chargingpoints_pic.png")

    st.markdown(
        f"""
        <h1 style='
            color: white;
            font-size: 64px;
            text-align: center;
            text-shadow: 0 0 5px #00ff00, 0 0 10px #00ff00, 0 0 15px #00ff00;
        '>Willkommen</h1>
        <div style='text-align: center; color: gray; margin-top: 80px; font-size: 16px;'>
            Entwickler: Frank Schulnies, Philipp Schauer, Thomas Baur
        </div>
        <div style='text-align: center; color: #cccccc; font-size: 12px; margin-top: 10px;'>
            Data Science Institute – by Fabian Rappert
        </div>
        """,
        unsafe_allow_html=True
    )

