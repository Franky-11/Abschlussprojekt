import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd

from cars_functions import read_df_fuel

st.set_page_config(layout="wide")




# ————— Funktionen —————
def berechne_auslastung(bev, ladepunkte, km, reichweite, ladezeit, ladeanteil):
    return ((km / reichweite) * (ladezeit / 60) * bev * ladeanteil) / ladepunkte

def berechne_schwellenwert(pkw, tankstellen, zapf, km, reichweite, tankzeit):
    return ((km / reichweite) * (tankzeit / 60) * pkw) / (tankstellen * zapf)

def gewichtete_ladezeit(normzeit, schnellzeit, schnellanteil):
    return schnellanteil * schnellzeit + (1 - schnellanteil) * normzeit

def plot_auslastung(bev_sim, auslastung_bev_sim, x_schnitt, y_schwelle, ladepunkte):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=bev_sim, y=auslastung_bev_sim,
        mode="lines", fill="tozeroy", name="Auslastung pro Ladepunkt (h/a)",
        line=dict(color="royalblue", width=2)
    ))

    fig.add_trace(go.Scatter(
        x=[auslastung_bev_sim[0], x_schnitt], y=[y_schwelle, y_schwelle],
        mode="lines", line=dict(color="gray", dash="dot"), showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[x_schnitt, x_schnitt], y=[0, y_schwelle],
        mode="lines", line=dict(color="gray", dash="dot"), showlegend=False
    ))

    fig.add_trace(go.Scatter(
        x=[x_schnitt], y=[y_schwelle],
        mode="markers+text", showlegend=False,
        marker=dict(color="crimson", size=8),
        text=[f"{x_schnitt/1E6:.1f} M BEV"],
        textposition="top right"
    ))

    fig.update_layout(
        xaxis_title="BEV-Fahrzeuge ",
        yaxis_title=" ∅ Auslastung pro Ladepunkt (h/a)",
        xaxis_range=[0, x_schnitt + 2_000_000],yaxis_range=[0, y_schwelle + 500] )

    fig.update_layout(hovermode="x unified")

    return fig

def info_box():
    st.markdown(
                f"""
                <div style="background-color:#1e1e1e;padding:16px;border-radius:6px;color:#ddd;">
                <h4>🔢 Formelübersicht</h4>
                <ol>
                    <li><strong>Auslastung pro Ladepunkt:</strong><br>
                        <code>Auslastung = ((km / Reichweite) × (Ladezeit / 60) × BEV × Anteil) / Ladepunkte</code>
                    </li>
                    <li><strong>Mittlere Ladezeit (gewichtet):</strong><br>
                        <code>Ladezeit = Anteil_Schnell × Schnellzeit + (1 - Anteil_Schnell) × Normalzeit</code>
                    </li>
                    <li><strong>Ladepunktbedarf für Zielauslastung:</strong><br>
                        <code>Ladepunkte = ((km / Reichweite) × (Ladezeit / 60) × BEV × Anteil) / Referenz-Auslastung</code>
                    </li>
                    <li><strong>Schwellenwert-Auslastung (Zapfsäule):</strong><br>
                        <code>Auslastung = ((km / Reichweite) × (Tankzeit / 60) × PKW) / (Tankstellen × Zapfsäulen)</code>
                    </li>
                </ol>
    
                <hr style="border: 0.5px solid #444;">
    
                <h4>🧮 Beispiel 1: Auslastung pro Ladepunkt</h4>
                <p style="font-size:0.95em">
                <strong>Eingaben:</strong><br>
                - BEV: 15 Mio.<br>
                - Anteil mit Ladebedarf: 20 %<br>
                - Fahrleistung: 12.000 km<br>
                - Reichweite: 300 km<br>
                - Ladezeit: 90 min<br>
                - Ladepunkte: 170.000<br><br>
    
                <strong>→ Auslastung:</strong><br>
                ((12.000 / 300) × (90 / 60) × 15.000.000 × 0.2) / 170.000 = <strong>1.058 h/a</strong>
                </p>
    
                <hr style="border: 0.5px solid #444;">
    
                <h4>🧮 Beispiel 2: Ladepunktbedarf bei gegebener BEV-Prognose</h4>
                <p style="font-size:0.95em">
                <strong>Eingaben:</strong><br>
                - BEV-Prognose: 15 Mio.<br>
                - Ladeanteil: 20 %<br>
                - Fahrleistung: 12.000 km<br>
                - Reichweite: 300 km<br>
                - Ladezeit: 100 min<br>
                - Ziel-Auslastung: 1.000 h/a<br><br>
    
                <strong>→ Ladepunktbedarf:</strong><br>
                ((12.000 / 300) × (100 / 60) × 15.000.000 × 0.2) / 1.000 = <strong>200.000 Ladepunkte</strong>
                </p>
    
                <span style="font-size:0.85em;color:#aaa;">
                Einheitliche Normierung auf jährliche Auslastung (h/a)
                </span>
                </div>
                """,
                unsafe_allow_html=True
            )







# ————— Oberfläche —————

if "szenario_df" not in st.session_state:
    st.session_state.szenario_df = pd.DataFrame()






st.header("⚡ Ladeinfrastruktur-Auslastung")


with st.container(border=True):
    with st.popover("📘 Berechnungsgrundlagen", use_container_width=True):
        info_box()

    col_bev,col_tank,col_prog=st.columns(3)
    # BEV-Parameter
    with col_bev:
        with st.popover("🔌 BEV-Parameter (öffentliches Laden)"):
            #bev = st.number_input("Anzahl BEV", value=1_650_000, step=100_000)
            ladepunkte = st.number_input("Anzahl Ladepunkte", value=170_000, step=10_000)
            jahres_km = st.number_input("Jahresfahrleistung (km)", value=12_000,step=1000)
            reichweite_bev = st.slider("Reichweite BEV (km)", 200, 500, 300)
            ladeanteil = st.slider("Anteil BEV mit Ladebedarf (%)", 0, 100, 20) / 100

            st.markdown("##### 🔄 Ladezeiten & Typ-Mix")
            normzeit = st.slider("⏱️ Ladezeit Normalladepunkt (min)", 120, 360, 120)
            schnellzeit = st.slider("⚡ Ladezeit Schnellladepunkt (min)", 10, 60, 30)
            schnellanteil = st.slider("Anteil Schnellladepunkte (%)", 0, 100, 27) / 100
            mittlere_ladezeit = gewichtete_ladezeit(normzeit, schnellzeit, schnellanteil)

            st.info(f"Mittlere Ladezeit: **{mittlere_ladezeit:.1f} min** bei {int(schnellanteil*100)} % Schnellladepunkten")
    with col_tank:
        # Schwellenwert-Parameter
        with st.popover("⛽ Referenz-Schwellenwert"):
           # pkw = st.number_input("Anzahl PKW", value=47_000_000)
           # tankstellen = st.number_input("Anzahl Tankstellen", value=14_800)
            #zapf = st.slider("Zapfsäulen je Tankstelle", 1, 20, 7)
            pkw = 47304737
            tankstellen = 14300
            zapf = 7
            st.markdown(
                f"""
                   <div style="background-color:#1e1e1e;padding:10px;border-radius:6px;">
                       <strong>🔧 Referenz: Verbrennerbasierte Auslastung</strong><br>
                       🚗 Verbrenner-Fahrzeuge: <strong>{pkw / 1E6:.1f} Mio.</strong><br>
                       ⛽ Zapfsäulen (gesamt): <strong>{(tankstellen * zapf) / 1E3:.1f} Tsd.</strong><br>
                       <span style="font-size: 0.9em; color: #666;">Aus diesen Werten wird die Auslastung (h/a) je Zapfsäule berechnet</span>
                   </div>
                   """,
                unsafe_allow_html=True
            )
            st.write("")
            reichweite = st.slider("Verbraucher-Reichweite (km)", 500, 900, 600)
            tankzeit = st.slider("Tankzeit (min)", 1, 30, 5)




            if st.checkbox("Eingabe Referenz-Auslastung"):
                y_schwelle=st.number_input("Referenz-Auslastung (h/a)", value=500, step=100)
            else:
                y_schwelle = berechne_schwellenwert(pkw, tankstellen, zapf, jahres_km, reichweite, tankzeit)

        st.metric(label="Ausgewählte Referenz-Auslastung pro Ladepunkt", value=f"{y_schwelle:,.0f} h/a")

            # Simulation

        bev_sim=np.arange(0,52,0.1)*1E6

        auslastung_bev_sim=berechne_auslastung(bev_sim, ladepunkte, jahres_km, reichweite_bev, mittlere_ladezeit, ladeanteil)           #((jahres_km/reichweite_bev)*(mittlere_ladezeit/60)*bev_sim*ladeanteil)/(ladepunkte)

        x_schnitt = float(np.interp(y_schwelle, auslastung_bev_sim, bev_sim))



    with col_prog:
        bev_prog = st.number_input("BEV-Fahrzeuge (Mio.)", value=1.65,step=1.0) * 1E6
        ladepunkt_bedarf_for_schwelle = ((jahres_km / reichweite_bev) * (
                    mittlere_ladezeit / 60) * bev_prog * ladeanteil) / (y_schwelle)
        ladepunkte_differenz = (ladepunkt_bedarf_for_schwelle - ladepunkte) / ladepunkte * 100

        st.metric(label=f"Bedarf Ladepunkte für Referenz-Auslastung von {y_schwelle:,.0f}h/a und {bev_prog/1e6:,.1f} Mio. BEV", value=f"{ladepunkt_bedarf_for_schwelle:,.0f}",
                  delta=f"{ladepunkte_differenz:,.1f}% in Bezug zu {ladepunkte:,.0f} Ladepunkten", delta_color="inverse")

    with col_bev:
        df_long = read_df_fuel()
        # bev_aktuell=df_long[df_long["Kraftstoff"] == "BEV"]["Wert"].max()
        auslastung_ladepunkt=berechne_auslastung(bev_prog, ladepunkte, jahres_km, reichweite_bev, mittlere_ladezeit, ladeanteil)
        diff_referenz_auslastung=(auslastung_ladepunkt-y_schwelle)/y_schwelle*100

        st.metric(f"∅ Auslastung pro Ladepunkt ",
                  value=f"{auslastung_ladepunkt:.0f} h/a",delta=f"{diff_referenz_auslastung:,.1f}% zur Referenz-Auslastung",delta_color="inverse")
        st.markdown(
            f"""
            **🔢 Parameterübersicht**  
            {bev_prog / 1e6:.1f} Mio. BEV • 
            Ladeanteil: {ladeanteil * 100:.0f}% • Ladepunkte: {ladepunkte:,.0f}
            """
        )

    st.write("")

    # ————— Plot —————
    st.markdown(
        f"""
        🚦 **Referenz-Auslastung:** {y_schwelle:,.0f} h/a<br>
        📍 **Erreicht bei:** {x_schnitt / 1E6:.0f} M BEV-Fahrzeugen<br>
        🔌 **Anzahl Ladepunkte:** {ladepunkte:,.0f}
        """,
        unsafe_allow_html=True
    )

    fig=plot_auslastung(bev_sim, auslastung_bev_sim, x_schnitt, y_schwelle, ladepunkte)
    st.plotly_chart(fig, use_container_width=True)



    if st.button("➕ Szenario speichern"):
        szenario_id = len(st.session_state.szenario_df) + 1

        df_row = pd.DataFrame([{
            "Szenario": szenario_id,
            "BEV-Fahrzeuge": bev_prog,
            "Anteil_Ladebedarf": ladeanteil,
            "Jahresfahrleistung (km)": jahres_km,
            "Reichweite_BEV (km)": reichweite_bev,
            "Ladepunkte": ladepunkte,
            "Ladezeit_Normal (min)": normzeit,
            "Ladezeit_Schnell (min)": schnellzeit,
            "Anteil_Schnell": schnellanteil,
            "Mittlere_Ladezeit (min)": int(mittlere_ladezeit),
            "Auslastung_Ladepunkt (h/a)": int(auslastung_ladepunkt),
            "Referenz_Auslastung (h/a)": int(y_schwelle),
            "BEV an Ref.-Auslastung": int(x_schnitt),
            "Bedarf Ladepunkte (bei Ref-Auslastung, BEV-Fahrzeuge)":int(ladepunkt_bedarf_for_schwelle)
        }])

        st.session_state.szenario_df = pd.concat([st.session_state.szenario_df, df_row], ignore_index=True)
        st.success("Szenario gespeichert.")

    if st.button("❌ Alle Szenarien löschen"):
        st.session_state.szenario_df = pd.DataFrame()
        st.warning("Alle Szenarien gelöscht.")




    with st.popover("📋 Szenarien-Tabelle", use_container_width=True):
        st.dataframe(
            st.session_state.szenario_df,
            hide_index=True,
            use_container_width=True
        )





