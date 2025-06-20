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

# --------------Fahrzeuge nach Kraftstoffart-------------------#

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



# --------------BEV-Fahrzeuge auf PLZ Ebene-------------------#
st.divider()


st.subheader("Verteilung BEV auf PLZ Ebene")
if 'plz_fig' not in st.session_state:
    st.session_state.plz_fig = None

col1,col2=st.columns([4,2])

with col1:
    with st.container(border=True):

        eingabe_plz = st.text_input("Geben Sie eine PLZ ein, um dorthin zu zoomen:", max_chars=5,
                                    placeholder="z.B. 06846")

        if st.button("Karte anzeigen") or st.session_state.plz_fig is None or eingabe_plz:
            with st.spinner("Lade Geodaten..."):
                geo_json_plz = read_geojson_plz()
            with st.spinner("Lade und mergen der Fahrzeug- und Geodaten......"):
                df_geo = read_df_geo()
                bev_kreise = read_df_cars_for_plz_map()
            default_center = {"lat": 51.0, "lon": 10.0}
            default_zoom = 5
            center_map = default_center
            zoom_level = default_zoom

            if eingabe_plz:
                eingabe_plz_formatted = str(eingabe_plz).strip().zfill(5)
                plz_row = bev_kreise[bev_kreise['PLZ'] == eingabe_plz_formatted]
                if not plz_row.empty:
                    center_map["lat"] = plz_row["lat"].iloc[0]
                    center_map["lon"] = plz_row["lon"].iloc[0]
                    zoom_level = 10
                    st.success(f"Karte wird auf PLZ {eingabe_plz_formatted} zentriert.")
                else:
                    st.warning(f"PLZ {eingabe_plz_formatted} nicht in den Daten gefunden. Zeige Gesamtkarte.")

            with st.spinner("Lade Karte..."):
                st.session_state.plz_fig=plot_car_plz_map(bev_kreise,zoom_level,center_map,geo_json_plz)
                st.plotly_chart(st.session_state.plz_fig)



with col2:
    df_cars_for_map = read_df_cars_for_map()
    land_max, anteil_max = df_cars_for_map.loc[df_cars_for_map['Anteil_BEV'].idxmax()][["Bundesland", "Anteil_BEV"]]
    land_min, anteil_min = df_cars_for_map.loc[df_cars_for_map['Anteil_BEV'].idxmin()][["Bundesland", "Anteil_BEV"]]

    st.markdown(":material/monitoring: **Key facts**")
    st.metric(label="Höchster Anteil BEV", value=f"{land_max} | {round(anteil_max,1)}%")
    st.metric(label="Niedrigster Anteil BEV", value=f"{land_min} | {round(anteil_min,1)}%")




# --------------BEV-nach Segmenten und Zulassungsentwicklung der Segemente und Gesamt-----------------------------#
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




# --------------Prognose BEV-----------------------------#


st.divider()

st.subheader("Prognose BEV-Fahrzeuge")

df_bev_prognose=read_df_bev_prognose()

col1,col2=st.columns([4,2])

with col1:
    tab1, tab2 = st.tabs([":material/stairs_2: BEV Prognose",":material/modeling: Prognose Fit"])
    with tab1:
        with st.container(border=True):
            fig=plot_prognose_bev(df_bev_prognose)
            st.plotly_chart(fig)

    with tab2:
        with st.container(border=True):
            #st.form()
           # L,k,x0=best_fit()

            if "plot_function" not in st.session_state:
                st.session_state.plot_function = False

            if "best_fit" not in st.session_state:
                st.session_state.best_fit = False
            if "L_const" not in st.session_state:
                st.session_state.L_const = False


            col3,col4=st.columns([1,3])
            with col3:
                with st.popover("Fitting Parameter"):
                    with st.form("Fitting"):
                        with st.expander(":material/info_i: Logistische Funktion"):
                            st.latex(r'''Y(t) = \frac{L}{1 + e^{-k \cdot (t - t_0)}}''')
                            st.markdown("**L**: Sättigungsgrenze\n\n**k**: Wachstumsrate\n\n**t_0**: Wendepunkt")

                        L=st.slider("Sättigung (Mio. BEV)",min_value=40,max_value=52,step=1)

                        k = st.slider("Wachstumsrate (1/Jahr)", 0.1, 0.5, 0.1)
                        x0 = st.slider("Wendepunkt (Jahr)", min_value=2025,max_value=2060,step=1)
                        x0=x0-2020
                        plot=st.form_submit_button('Plot function')
                        if st.checkbox("L const."):
                            st.session_state.L_const = True
                        if plot:
                            st.session_state.plot_function=True
                        if st.checkbox("Best Fit"):
                            st.session_state.best_fit=True

            if st.session_state.plot_function and not st.session_state.best_fit and not st.session_state.L_const:
                fig = plot_data_and_fit(L, k, x0, True)
                st.plotly_chart(fig)
                with col4:
                    show_paramater(L,k,x0)
            elif st.session_state.best_fit and not st.session_state.L_const:
                L,k,x0=best_fit()
                fig = plot_data_and_fit(L, k, x0, True)
                st.plotly_chart(fig)
                with col4:
                    show_paramater(L,k,x0)
                st.session_state.best_fit=False

            elif st.session_state.L_const and st.session_state.best_fit:
                L_const=L
                fixed_L,k,x0=best_fit(fixed_L=L_const)
                fig=plot_data_and_fit(fixed_L, k, x0, True)
                st.plotly_chart(fig)
                with col4:
                    show_paramater(fixed_L,k,x0)
                st.session_state.best_fit = False
                st.session_state.L_const=False

            else:
                fig = plot_data_and_fit(L, k, x0, False)
                st.plotly_chart(fig)



with col2:
    st.markdown(":material/monitoring: **Key facts**")
    st.metric(label="Ziel Bundesregierung bis 2030",
              value=f"{15}Mio. BEV",delta=f"∆ {(15-1.65)}",delta_color="inverse")
    st.divider()

    st.markdown("""
            **🔌Einbindung chinesischer Automobilhersteller**<br>
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; verstärkte Marktpräsenz dieser Hersteller ist wichtig für einen
            &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;umfassenden Hochlauf von Elektromobilität
            """, unsafe_allow_html=True)

    st.markdown("""
                   **🔌Ladeinfrastruktur ist unerlässlich**<br>
                   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  muss dem Markthochlauf der BEV vorauslaufen
                   """, unsafe_allow_html=True)

    st.markdown("""
                      **🔌Erweitertes Angebot an BEV-Modellen**<br>
                      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  insbesondere in den unteren Preiskategorien (Klein- und
                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Kompaktwagen) ist essenziell
                      """, unsafe_allow_html=True)

    st.markdown("""
                          **🔌Investitionen in Forschung und Entwicklung**<br>
                          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Batterietechnologien, Integration von Elektrofahrzeugen als 
                          &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;mobile Zwischenspeicher für Strom (bidirektionales Laden)
                          """, unsafe_allow_html=True)


