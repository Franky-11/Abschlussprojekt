import streamlit as st
from cars_functions import *
import time

if 'animation_active' not in st.session_state:
    st.session_state.animation_active = False

if 'animation_finished' not in st.session_state:
    st.session_state.animation_finished = False

if 'percent_checked' not in st.session_state:
    st.session_state.percent_checked = False

if 'annot_checked' not in st.session_state:
    st.session_state.annot_checked = False

df = read_df_cars()

st.header("Fahrzeugbestand")

col1,col2=st.columns([2.3,1.5])



with col2:
    st.header("")
    st.image("images/cars_2.jpg",use_container_width=True)#width=300)

with col1:
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
                start_button_clicked=st.button("Start")
                status_placeholder = st.empty()
            with col2:
                st.checkbox("Anteil E-Car", key="percent_checked")
                st.checkbox("Events", key="annot_checked")
               # st.session_state.percent_checked=st.checkbox("Anteil E-Car",value=st.session_state.percent_checked, key="percent_checkbox")
               # st.session_state.annot_checked = st.checkbox("Events", value=st.session_state.annot_checked, key="events_checkbox")

            plot_placeholder = st.empty()

            if start_button_clicked:
                st.session_state.animation_active = True
                st.session_state.animation_finished = False

            if st.session_state.animation_active:
                for i in range(1, len(df)+1):
                    df_filtered=df.iloc[-i::]
                    growth_factor = (df_filtered["e_cars"].iloc[0] / df_filtered["e_cars"].iloc[-1])
                    status_placeholder.markdown(f"##### :material/arrow_upward: {growth_factor:.0f}-fache")
                    fig2 = plot_e_cars(df_filtered,False)
                    plot_placeholder.plotly_chart(fig2)
                    time.sleep(0.1)

                st.session_state.animation_active = False
                st.session_state.animation_finished = True
                st.rerun()

            if not st.session_state.animation_active:
                fig=None
                if st.session_state.percent_checked:
                    fig=plot_e_cars_percent(df,False)
                    if st.session_state.annot_checked:
                        fig=plot_e_cars_percent(df,True)

                elif st.session_state.annot_checked:
                    fig=plot_e_cars(df,True)

                elif st.session_state.animation_finished:
                    fig = plot_e_cars(df,False)
                    growth_factor = (df["e_cars"].iloc[0] / df["e_cars"].iloc[-1])
                    status_placeholder.markdown(f"##### :material/arrow_upward: {growth_factor:.0f}-fache")
                if fig is not None:
                    plot_placeholder.plotly_chart(fig)





