import streamlit as st
from cars_functions import *

df = read_df_cars()

st.header("Fahrzeugbestand")

tab1, tab2 = st.tabs(["PKW Gesamt", "E-Car"])

with tab1:
    with st.container(border=True,height=520):
        change=(df["cars_sum"].iloc[0]-df["cars_sum"].iloc[-1])/df["cars_sum"].iloc[-1]*100
        st.markdown(f"##### :material/trending_up: {change:.1f}%")
        fig1=plot_cars(df)
        st.plotly_chart(fig1)

with tab2:
    with st.container(border=True,height=520):
        col1,col2=st.columns([1,3])
        with col1:
            growth_factor = (df["e_cars"].iloc[0]/df["e_cars"].iloc[-1])
            st.markdown(f"##### :material/arrow_upward: {growth_factor:.0f}-fache")


        with col2:
            percent=st.checkbox("Anteil E-Car")
        fig2=plot_e_cars(df,percent)
        st.plotly_chart(fig2)