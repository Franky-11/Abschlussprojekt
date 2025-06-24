import streamlit as st
import pandas as pd
import plotly.graph_objects as go
""""
def strombedarf_szenarien(fahrzeuge,verbrauch,jahres_km):
    return fahrzeuge*verbrauch*(jahres_km/100)



def run():
    st.title("🔌 Strombedarf-Simulator")
    st.markdown("Berechne den jährlichen Strombedarf bei vollständiger Elektrifizierung des Straßenverkehrs.")

    st.sidebar.header("📊 Eingaben")
    szenario = st.sidebar.radio("Szenario", ["2025", "2030", "2035"])
    fahrzeuge = st.sidebar.slider("Fahrzeuganzahl (in Mio.)", 1, 52, 15) * 1_000_000
    verbrauch = st.sidebar.slider("Verbrauch (kWh / 100 km)", 10, 25, 20)
    jahres_km = st.sidebar.slider("Jahresfahrleistung (km)", 8000, 20000, 12000)
    lastmanagement = st.sidebar.checkbox("Lastmanagement aktivieren")

    if szenario=="2025":
        strombedarf = strombedarf_szenarien(1.7*1_000_000,18, 12000)
        strombedarf_twh = strombedarf / 1e9
    elif szenario=="2030":
        strombedarf = strombedarf_szenarien(15*1_000_000,18, 12000)
        strombedarf_twh = strombedarf / 1e9
    elif szenario=="2035":
        strombedarf = strombedarf_szenarien(35 *1_000_000,18, 12000)
        strombedarf_twh = strombedarf / 1e9


    st.metric("🔋 Strombedarf gesamt", f"{strombedarf_twh:.2f} TWh")

    df = pd.DataFrame({
        "Szenario": [szenario],
        "Fahrzeuge": [fahrzeuge],
        "Verbrauch (kWh/km)": [verbrauch],
        "Jahres-km": [jahres_km],
        "Lastmanagement": [lastmanagement],
        "Strombedarf (TWh)": [strombedarf_twh]
    })

    st.download_button("📥 Ergebnisse als CSV herunterladen", df.to_csv(index=False), file_name="strombedarf_szenario.csv", mime="text/csv")

    # --- Plotly Stacked Bar Chart: Strombedarf vs. EE ---
    import plotly.graph_objects as go

    jahre = list(range(2025, 2036))
    bev_bedarf = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]  # BEV-Bedarf in TWh
    ee_erzeugung = [260, 275, 290, 305, 320, 340, 360, 375, 385, 395, 400]
    rest_ee = [ee - bev for ee, bev in zip(ee_erzeugung, bev_bedarf)]

    fig = go.Figure()
    fig.add_trace(go.Bar(name="BEV-Strombedarf", x=jahre, y=bev_bedarf))
    fig.add_trace(go.Bar(name="Restliche EE-Erzeugung", x=jahre, y=rest_ee))

    fig.update_layout(
        barmode='stack',
        title="Strombedarf der E-Mobilität vs. EE-Erzeugung (2025–2035)",
        xaxis_title="Jahr",
        yaxis_title="Energie (TWh)"
    )

    st.plotly_chart(fig, use_container_width=True)

"""
def strombedarf_szenarien(fahrzeuge,verbrauch,jahres_km):
    return fahrzeuge*verbrauch*(jahres_km/100)

def run():
    st.title("🔌 Strombedarf-Simulator")
    st.markdown("Berechne den jährlichen Strombedarf bei vollständiger Elektrifizierung des Straßenverkehrs.")

    st.sidebar.header("📊 Eingaben")
    szenario = st.sidebar.radio("Szenario", ["2025", "2030", "2035"])
    fahrzeuge = st.sidebar.slider("Fahrzeuganzahl (in Mio.)", 1, 52, 15) * 1_000_000
    verbrauch = st.sidebar.slider("Verbrauch (kWh / 100 km)", 10, 25, 20)
    jahres_km = st.sidebar.slider("Jahresfahrleistung (km)", 8000, 20000, 12000)
    lastmanagement = st.sidebar.checkbox("Lastmanagement aktivieren")

    # Slider-Eingaben statt feste Szenario-Werte verwenden
    strombedarf = strombedarf_szenarien(fahrzeuge, verbrauch, jahres_km)
    strombedarf_twh = strombedarf / 1e9

    st.metric("🔋 Strombedarf gesamt", f"{strombedarf_twh:.2f} TWh")

    df = pd.DataFrame({
        "Szenario": [szenario],
        "Fahrzeuge": [fahrzeuge],
        "Verbrauch (kWh/km)": [verbrauch],
        "Jahres-km": [jahres_km],
        "Lastmanagement": [lastmanagement],
        "Strombedarf (TWh)": [strombedarf_twh]
    })

    st.download_button("📥 Ergebnisse als CSV herunterladen", df.to_csv(index=False), file_name="strombedarf_szenario.csv", mime="text/csv")

    # --- Plotly Stacked Bar Chart: Strombedarf vs. EE ---
    jahre = list(range(2025, 2036))
    bev_bedarf = [30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]
    ee_erzeugung = [260, 275, 290, 305, 320, 340, 360, 375, 385, 395, 400]
    rest_ee = [ee - bev for ee, bev in zip(ee_erzeugung, bev_bedarf)]

    # Aktuellen Nutzerwert im Szenariojahr einfügen
    jahr_index = jahre.index(int(szenario))
    bev_bedarf[jahr_index] = strombedarf_twh
    rest_ee[jahr_index] = max(0, ee_erzeugung[jahr_index] - strombedarf_twh)

    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="🔋 BEV-Strombedarf",
        x=jahre,
        y=bev_bedarf,
        marker_color="#636EFA"
    ))
    fig.add_trace(go.Bar(
        name="🌿 Restliche EE-Erzeugung",
        x=jahre,
        y=rest_ee,
        marker_color="#00CC96"
    ))

    fig.update_layout(
        barmode='stack',
        title="⚡ Strombedarf der E-Mobilität vs. EE-Erzeugung (2025–2035)",
        xaxis_title="Jahr",
        yaxis_title="Energie (TWh)",
        template="plotly_white",
        legend=dict(orientation="h", y=1.1, x=0.5, xanchor="center", yanchor="bottom"),
        height=500
    )

    st.plotly_chart(fig, use_container_width=True)