import streamlit as st
from datetime import timedelta




st.subheader("TCO - Total Cost Ownership")





st.audio("audio/TCO_Vergleich_2.wav",format="audio/wav",start_time=timedelta(seconds=98))

with st.popover("Quellen anzeigen"):
    st.markdown("""
        **NOW GmbH / Fraunhofer ISI** (im Auftrag des Bundesministeriums für Digitales und Verkehr (BMDV). (März 2023).  
         *FACTSHEET TCO: Eine Wirtschaftlichkeitsanalyse der Antriebsarten für Pkw*.
        """)
