import streamlit as st
from cars_functions import *
import time

from cars_functions import read_geojson



if 'annot_checked' not in st.session_state:
    st.session_state.annot_checked = False



col1,col2=st.columns([2,3])
with col1:
    st.header("")
    st.write("")

    st.header("Fahrzeugbestand")

with col2:
    st.image("images/cars_2.jpg",width=300)

st.divider()

col1,col2=st.columns([4,2])


df = read_df_fuel()

with col1:
    tab1, tab2 = st.tabs([":material/directions_car: PKW nach Kraftstoffart", "# :material/electric_car: BEV-Fahrzeuge"])
    with tab1:
        with st.container(border=True, height=550):
            fig1 = plot_car_fuel(df)
            st.plotly_chart(fig1)

    with tab2:
        with st.container(border=True,height=550):
            event_col,pop_col=st.columns([1,3])
            with event_col:
                st.checkbox("Events", key="annot_checked")
            with pop_col:
                with st.popover(":material/moving: Neuzulassungen BEV",use_container_width=True):
                    df_neu_bev = read_df_neu_bev()
                    fig3 = plot_neu_bev(df_neu_bev)
                    st.metric("Neuzulassungen 2024",value="380 Tsd.",delta="-27%")
                    st.plotly_chart(fig3)
            fig2=plot_bev(df,st.session_state.annot_checked)
            st.plotly_chart(fig2)





with col2:
    st.markdown(":material/monitoring: **Key facts**")
    st.metric(label="Gesamtbestand PKW 2025", value="49.3 Mio.", delta="+0.49% zum Vorjahr",delta_color="normal")
    st.subheader("")

    st.metric(label="BEV-Fahrzeuge 2025", value="1.65 Mio. | Anteil 3.3 %", delta="+17.7% zum Vorjahr", delta_color="normal")




st.divider()

st.subheader("BEV-Fahrzeuge nach Bundesländern")


df_cars_for_map=read_df_cars_for_map()
geojson=read_geojson()

col1,col2=st.columns([4,2])

with col1:
    with st.container(border=True):
        fig=plot_car_map(df_cars_for_map,geojson)
        st.plotly_chart(fig)

with col2:
    land_max, anteil_max = df_cars_for_map.loc[df_cars_for_map['Anteil_BEV'].idxmax()][["Bundesland", "Anteil_BEV"]]
    land_min, anteil_min = df_cars_for_map.loc[df_cars_for_map['Anteil_BEV'].idxmin()][["Bundesland", "Anteil_BEV"]]

    st.markdown(":material/monitoring: **Key facts**")
    st.metric(label="Höchster Anteil BEV", value=f"{land_max} | {round(anteil_max,1)}%")
    st.subheader("")
    st.metric(label="Niedrigster Anteil BEV", value=f"{land_min} | {round(anteil_min,1)}%")


    #st.metric(label="Höchster Anteil BEV", value=f"{land_max} ({anteil_max}%)")

st.divider()

st.subheader("BEV-Neuzulassungen")


st.divider()

st.subheader("Prognose BEV-Fahrzeuge")
