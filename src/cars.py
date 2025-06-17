import streamlit as st
from cars_functions import *
import time

#from cars_functions import read_geojson



if 'annot_checked' not in st.session_state:
    st.session_state.annot_checked = False



col1,col2=st.columns([4,2])
with col1:
    st.header("")
    st.write("")

    st.title("Fahrzeugbestand :material/directions_car:")

with col2:

    st.image("images/cars_2.jpg",use_container_width=True)

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
                    st.markdown(" **:material/euro: :material/account_balance: Markt abhängig von staatlichen Anreizen**")
                    st.plotly_chart(fig3)




            fig2=plot_bev(df,st.session_state.annot_checked)
            st.plotly_chart(fig2)


with col2:
    st.markdown(":material/monitoring: **Key facts**")
    st.metric(label="Gesamtbestand PKW 2025", value="49.3 Mio.", delta="+0.49% zum Vorjahr",delta_color="normal")
    st.metric(label="BEV-Fahrzeuge 2025", value="1.65 Mio. | Anteil 3.3 %", delta="+17.7% zum Vorjahr", delta_color="normal")
    #st.subheader("")

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
    st.metric(label="Niedrigster Anteil BEV", value=f"{land_min} | {round(anteil_min,1)}%")


    #st.metric(label="Höchster Anteil BEV", value=f"{land_max} ({anteil_max}%)")

st.divider()

st.subheader("BEV nach Segmenten")
df_long=read_df_bev_segmente()
df_sorted=read_df_bev_segmente(long=False)
df_neu_bev_segment=read_df_bev_zulassung_segmente()

col1,col2=st.columns([4,2])
with col1:
    tab1, tab2,tab3 = st.tabs(
        [":material/pie_chart: Segmentanteile 2025","# :material/electric_car: Anteil BEV an Neuzulassungen", "# :material/electric_car: BEV-Anteile in Segmenten 2025"])

    with tab1:
        with st.container(border=True):
            fig=plot_bev_segmente(df_long)
            st.plotly_chart(fig)


    with tab2:
        with st.container(border=True):
            segments=st.multiselect("Auswahl Segment",options=df_neu_bev_segment["Segment"].unique().tolist(),default=["OBERE MITTELKLASSE","KLEINWAGEN","MINIS"])
            fig=plot_bev_zulassung_segmente(df_neu_bev_segment,segments)
            st.plotly_chart(fig)


    with tab3:
        with st.container(border=True):
            fig=plot_bev_penetration(df_sorted)
            st.plotly_chart(fig)

with col2:
    st.markdown(":material/monitoring: **Key facts**")

    st.metric(label="Starke Verschiebung der Segment-Dominanz bei BEV", value=f"{round(df_long["Wert"].max(),1)}% | SUVs")
    st.markdown("------------------------------------------")
    st.markdown("""
           **🔌 Trend zu größeren, energieintensiveren<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Fahrzeugen bei BEV**<br>
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;könnte Effizienzgewinne der<br>
           &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Elektromobilität teilweise untergraben
           """, unsafe_allow_html=True)

    st.markdown("""
        **🔌Höchste BEV-Penetration**<br>
        &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Oberklasse, SUVs & Minis
        """,unsafe_allow_html=True)
    st.markdown("""
           **🔌Neuzulassungen BEV**<br>
          &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Minis & Kleinwagen rückläufig<br>
         &nbsp; &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 
            """, unsafe_allow_html=True)







st.divider()

st.subheader("Prognose BEV-Fahrzeuge")
