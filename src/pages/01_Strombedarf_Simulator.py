import streamlit as st
import plotly.express as px
import sys, pathlib

# füge das übergeordnete Verzeichnis zu sys.path hinzu,
# damit Python dort strombedarf.py findet
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from strombedarf import strombedarf_szenarien

st.title("⚡ Strombedarf-Simulator")

bev_mio = st.slider(
    "Wie viele BEV im Bestand?",
    min_value=0,
    max_value=50,
    value=15,
    help="Ziel der Bundesregierung: 15 Mio. BEV bis 2030"
)

results = strombedarf_szenarien(bev_count=bev_mio * 1_000_000)
base = results["basis"]
opt  = results["optimistisch"]
pes  = results["pessimistisch"]

st.metric("Jährlicher Strombedarf (Basis-Szenario)", f"{base:.1f} TWh")

fig = px.bar(
    x=["Optimistisch", "Basis", "Pessimistisch"],
    y=[opt, base, pes],
    labels={"x": "Szenario", "y": "Strombedarf [TWh]"},
    text_auto=".1f"
)
st.plotly_chart(fig, use_container_width=True)

st.info(
    "Zum Vergleich: Der deutsche Bruttostromverbrauch 2024 lag bei rund 500 TWh."
)