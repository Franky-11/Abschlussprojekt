import streamlit as st
from cars_functions import *
import time

df = read_df_cars()

st.header("Fahrzeugbestand")

tab1, tab2 = st.tabs(["PKW Gesamt", "E-Car"])

with tab1:
    with st.container(border=True,height=550):
        change=(df["cars_sum"].iloc[0]-df["cars_sum"].iloc[-1])/df["cars_sum"].iloc[-1]*100
        st.markdown(f"##### :material/trending_up: {change:.1f}%")
        fig1=plot_cars(df)
        st.plotly_chart(fig1)

with tab2:
    with st.container(border=True,height=550):
        col1,col2=st.columns([1,3])
        with col1:
            button=st.button("Start")
            status_placeholder = st.empty()
        with col2:
            percent=st.checkbox("Anteil E-Car")

        plot_placeholder = st.empty()

        if button:
            for i in range(1, len(df)+1):
                df_filtered=df.iloc[-i::]
                growth_factor = (df_filtered["e_cars"].iloc[0] / df_filtered["e_cars"].iloc[-1])
                status_placeholder.markdown(f"##### :material/arrow_upward: {growth_factor:.0f}-fache")
                fig3 = plot_e_cars(df_filtered)
                plot_placeholder.plotly_chart(fig3)
                time.sleep(0.1)
        elif percent:
            fig4=plot_e_cars_percent(df)
            st.plotly_chart(fig4)
        else:
            fig2=plot_e_cars(df.loc[[df.index[-1], df.index[-2], df.index[0]]])
            st.plotly_chart(fig2)

