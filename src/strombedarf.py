import streamlit as st

from strombedarf_functions import *

def run():

    col1,col2=st.columns([1,1])
    with col1:
        st.header("")
        st.write("")

        st.title("Strombedarf:material/electric_bolt:")

    with col2:
        st.image("images/electricity-2595842_1280.jpg",use_container_width=True)


    st.divider()


    #--------------Frank Stromverbrauch BEV-----------"

    col1,col2=st.columns([4,2])


    with col1:
        tab1, tab2,tab3,tab4 = st.tabs([":material/battery_low: Stromverbrauch BEV", ":material/query_stats: Vergleich Quantile",":material/gesture_select: Vergleich Modelle",":material/distance: ∅ Reichweite"])
        with tab1:
            with st.container(border=True, height=500):
                df_verbrauch=read_verbrauchsdaten()
                desc_stats = df_verbrauch.groupby(["Segment", "Testart"])[
                    "Verbrauch_(kWh/100km)"].describe().reset_index().sort_values(by=["Segment","mean"])
                with st.popover("Deskriptive Statistik",use_container_width=True):
                    st.dataframe(desc_stats.round(1),hide_index=True,use_container_width=True)
                fig=plot_verbrauch(df_verbrauch)
                st.plotly_chart(fig)


        with tab2:
            with st.container(border=True,height=500):
                fig=plot_quantile(df_verbrauch)
                st.plotly_chart(fig)

        with tab3:
            with st.container(border=True,height=650):
                with st.popover("Segmente auswählen"):
                    with st.form("Modellauswahl"):
                        check_col1,check_col2=st.columns(2)
                        with check_col1:
                            mini=st.checkbox("Minis & Kleinwagen")
                            kompakt=st.checkbox("Kompaktklasse")
                            mittel=st.checkbox("Mittelklasse")
                            obere=st.checkbox("Obere Mittelklasse & Oberklasse")
                        with check_col2:
                            suv=st.checkbox("SUVs & Geländewagen")
                            uti=st.checkbox("Utilities, Mini-Vans & Großraum-Vans")
                            sonst=st.checkbox("Sonstige")

                        seg = df_verbrauch["Segment"].unique().tolist()
                        check_list = [mini, kompakt, mittel, obere, suv, uti, sonst]
                        seg_filtered = segments(check_list, seg)
                        df_filtered_seg = segment_filter(df_verbrauch, seg_filtered)
                        modelle = sorted(df_filtered_seg["Modell"].unique().tolist())
                        st.form_submit_button("Segmente auswählen")

                selected_modell = st.multiselect("Modelle", options=modelle, default=modelle[0:3])
                df_modell_filtered=modell_filter(df_filtered_seg,selected_modell)

                if df_modell_filtered.empty:
                    selected_modell = ["Renault Twingo Z.E.","Tesla Model 3 Long Range AWD","Mercedes EQV 300"]
                    fig=plot_modell_verbrauch(df_verbrauch[(df_verbrauch["Modell"].isin(selected_modell)) & (df_verbrauch["Testart"]=="Realer Verbrauch")])
                else:
                    df_modell_filtered = modell_filter(df_filtered_seg, selected_modell)
                    fig = plot_modell_verbrauch(df_modell_filtered)
                st.plotly_chart(fig)
        with tab4:
            with st.container(border=True,height=500):
                df_reichweite=read_reichweite()
                fig=plot_reichweite(df_reichweite)
                st.plotly_chart(fig)




    stats = df_verbrauch.groupby("Testart")["Verbrauch_(kWh/100km)"].describe().reset_index()
    delta=(stats.loc[0,"mean"]-stats.loc[1,"mean"])/stats.loc[1,"mean"]*100
    mini=stats.loc[0,"min"]
    maxi=stats.loc[0,"max"]

    max_reichweite=df_reichweite["Durchschnittliche Reichweite (km)"].max()
    min_reichweite=df_reichweite["Durchschnittliche Reichweite (km)"].min()
    delta_reichweite=(max_reichweite-min_reichweite)/min_reichweite*100

    with col2:
        st.markdown(":material/monitoring: **Key facts**")

        st.metric(label="Mittlerer Verbrauch BEV",value=f"{stats.loc[0,"mean"]:.1f} kWh/100km",delta=f"{delta:.1f}% zum WLTP",delta_color="inverse")

        st.write("")

        st.metric(label=" ∅ Reichweite BEV", value=f"{max_reichweite} km",
                  delta=f"{delta_reichweite:.0f}% zu 2014", delta_color="normal")



        #st.markdown("------------------------------------------")



