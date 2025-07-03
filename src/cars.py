import streamlit as st
from cars_functions import *
import time
from watermarks import set_watermark



#from cars_functions import read_geojson

def run():
    set_watermark("images/watermark/cars.jpg")
    if 'annot_checked' not in st.session_state:
        st.session_state.annot_checked = False



#    col1,col2=st.columns([4,2])
#    with col1:
#        st.header("")
#        st.write("")

    st.title("Fahrzeugmarkt :material/directions_car:")

#    with col2:

#        st.image("images/cars_2.jpg",use_container_width=True)

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
                with st.popover("Quellen anzeigen"):
                    st.markdown("**Kraftfahrzeugbundesamt**")

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
        st.write("")
        st.metric(label="BEV-Fahrzeuge 2025", value="1.65 Mio. | Anteil 3.3 %", delta="+17.7% zum Vorjahr", delta_color="normal")
        #st.subheader("")



    # --------------BEV-Fahrzeuge auf Kreis  Ebene-------------------#

    if "selected_laender" not in st.session_state:
        st.session_state.selected_laender = ["Alle"]

    st.divider()


    st.subheader("Verteilung BEV auf Kreisebene")
    col1, col2 = st.columns([4, 2])

    with col1:
        geojson_kreise=read_geojson_landkreise()
        df_kreise_land=read_df_kreise_land()

        with st.container(border=True):
            col_select,col_df=st.columns(2)
            with col_select:
                with st.popover("Auswahl Bundesländer"):
                    with st.form("Auswahl Bundesländer"):
                        options=df_kreise_land["Bundesland"].unique().tolist()+["Alle"]
                        selected_laender=st.multiselect("Auswahl Bundesländer",options=options,default=st.session_state.selected_laender)
                        if st.form_submit_button("Auswählen"):
                            st.session_state.selected_laender=selected_laender

                    if "Alle" in selected_laender:
                        df_filtered=df_kreise_land
                    else:
                        df_filtered=df_kreise_land[df_kreise_land["Bundesland"].isin(selected_laender)]
            with col_df:
                with st.popover("Daten Bundesländer"):
                    info=info_bundesland(df_filtered)
                    st.dataframe(info,use_container_width=True,hide_index=True)

            fig=plot_bev_kreise(df_filtered,geojson_kreise)
            st.plotly_chart(fig)
            with st.popover("Quellen anzeigen"):
                st.markdown("""**Kraftfahrzeugbundesamt**    
                Geojson:  OpenDataLab""")







    with col2:
        df_cars_for_map = read_df_cars_for_map()
        land_max, anteil_max = df_cars_for_map.loc[df_cars_for_map['Anteil_BEV'].idxmax()][["Bundesland", "Anteil_BEV"]]
        land_min, anteil_min = df_cars_for_map.loc[df_cars_for_map['Anteil_BEV'].idxmin()][["Bundesland", "Anteil_BEV"]]

        st.markdown(":material/monitoring: **Key facts**")
        st.metric(label="Höchster Anteil BEV", value=f"{land_max} | {round(anteil_max,1)}%")
        st.write("")
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
                with st.popover("Quellen anzeigen"):
                    st.markdown("**Kraftfahrzeugbundesamt**")


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
               **🔌 Trend zu größeren, energieintensiveren Fahrzeugen bei BEV**<br>
               könnte Effizienzgewinne der Elektromobilität teilweise untergraben
               """, unsafe_allow_html=True)

        st.markdown("""
            **🔌Höchste BEV-Penetration**<br>
            Oberklasse, SUVs & Minis
            """,unsafe_allow_html=True)
        st.markdown("""
               **🔌Neuzulassungen BEV**<br>
             Minis & Kleinwagen rückläufig
                """, unsafe_allow_html=True)

    #----------------TCO------------#

    st.divider()

    st.subheader("TCO - Total Cost Ownership")
    col1, col2 = st.columns([4, 2])
    with col1:
        with st.container(border=True):
            fig=tco_info()
            st.plotly_chart(fig, use_container_width=True)
            with st.popover("Quellen anzeigen"):
                st.markdown("""
                    * ADAC Vergleich Gesamtkosten E-Auto vs. Verbrenner:  
                    https://www.adac.de/rund-ums-fahrzeug/auto-kaufen-verkaufen/autokosten/elektroauto-kostenvergleich/#vergleich-e-auto-vs-verbrenner
                    * FACTSHEET TCO:  **NOW GmbH / Fraunhofer ISI** (im Auftrag des Bundesministeriums für Digitales und Verkehr (BMDV). (März 2023).  
                     *FACTSHEET TCO: Eine Wirtschaftlichkeitsanalyse der Antriebsarten für Pkw*.
                    """)

    with col2:
        st.markdown(":material/monitoring: **Key facts**")
        st.markdown("🔌BEV der Mittelklasse und SUVs oft günstiger als ihre jeweiligen Verbrenner-Pendants")
        st.markdown("🔌BEV-Kleinwagen oft nicht konkurrenzfähig gegenüber Verbrenner, erst späte Kostenparität ")
        st.markdown("🔌Erst bei sinkenden Stromkosten und geringeren Kaufpreisen dürften E-Autos in der Gesamtkostenbilanz wieder mithalten")
        st.write("")
        st.markdown("🔌 Podcast zum Factsheet TCO (NOW GmbH / Fraunhofer ISI)")
        st.audio("audio/TCO_Vergleich_2.wav", format="audio/wav")



    # --------------Prognose BEV-----------------------------#


    st.divider()

    st.subheader("Prognose BEV-Fahrzeuge")

    df_bev_prognose=read_df_bev_prognose()

    col1,col2=st.columns([4,2])

    with col1:
        tab1, tab2 = st.tabs([":material/stairs_2: BEV Prognose",":material/modeling: Prognose Fit"])
        with tab1:
            with st.container(border=True,height=550):
                fig=plot_prognose_bev(df_bev_prognose)
                st.plotly_chart(fig)
                with st.popover("Quellen anzeigen"):
                    st.write("Studien")
                    st.markdown("""
                                   * **Agora Verkehrswende (Boston Consulting Group):** "Letzte Chance für 15 Millionen E-Autos bis 2030" (Langfassung).
                                   * **Bundesverband Erneuerbare Energie e.V. (BEE):** "BEE-Mobilitätsszenarien 2045 – Eine Analyse von drei Szenarien zum Umsetzen der Klimaschutzziele bis 2045".
                                   * **e-mobil BW GmbH, NRW.Energy4Climate GmbH (P3 automotive GmbH, Boesche Rechtsanwälte PartGmbB):** "Bidirektionales Laden in Deutschland: Marktentwicklung und Potenziale".
                                   * **Nationale Leitstelle Ladeinfrastruktur (NOW GmbH, Reiner Lemoine Institut gGmbH):** "Ladeinfrastruktur nach 2025/2030: Szenarien für den Markthochlauf – Neuauflage 2024".
                                   * **Intraplan, Trimode, MWP, ETR (im Auftrag des BMDV):** "Verkehrsprognose 2040 Band 6.1 E: Verkehrsentwicklungsprognose – Prognosefall 1 „Basisprognose 2040“ (Ergebnisse)".
                                   """)

        with tab2:
            with st.container(border=True,height=550):
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
                    with st.popover("Fit Parameter"):
                        with st.form("Logistische Funktion"):
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
                verstärkte Marktpräsenz dieser Hersteller ist wichtig für einen
                umfassenden Hochlauf von Elektromobilität
                """, unsafe_allow_html=True)

        st.markdown("""
                       **🔌Ladeinfrastruktur ist unerlässlich**<br>
                       muss dem Markthochlauf der BEV vorauslaufen
                       """, unsafe_allow_html=True)

        st.markdown("""
                          **🔌Erweitertes Angebot an BEV-Modellen**<br>
                          insbesondere in den unteren Preiskategorien (Klein- und
                        Kompaktwagen) ist essenziell
                          """, unsafe_allow_html=True)

        st.markdown("""
                              **🔌Investitionen in Forschung und Entwicklung**<br>
                              Batterietechnologien, Integration von Elektrofahrzeugen als 
                              mobile Zwischenspeicher für Strom (bidirektionales Laden)
                              """, unsafe_allow_html=True)


#st.set_page_config(layout="wide")
#run()
