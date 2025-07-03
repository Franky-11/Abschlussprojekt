import streamlit as st
import matplotlib.pyplot as plt
from watermarks import set_watermark
set_watermark("images/watermark/chargingpoints_pic.png")
from matplotlib.ticker import FuncFormatter

from chargingpoints_functions import load_data
from chargingpoints_functions import berechne_entwicklung
from chargingpoints_functions import berechne_entwicklung_nach_art
from chargingpoints_functions import prognose_linear_referenz



def run():
    # Initialisierung der Session-State-Flags
    if 'prognose_aktiv' not in st.session_state:
        st.session_state['prognose_aktiv'] = False
    if 'demand_aktiv' not in st.session_state:
        st.session_state['demand_aktiv'] = False

    df = load_data()

    # Basisdaten
    _df_kum_lp = berechne_entwicklung("Anzahl Ladepunkte", df)
    df_kum_lp = _df_kum_lp
    # kumulierte Entwicklung nach Typ
    _df_group = berechne_entwicklung_nach_art(df)
    df_group_cum = _df_group.cumsum()

    st.title("Ladeinfrastruktur Deutschland :material/ev_station: – Ist, Soll und Bedarf")

    # Erstes Diagramm: kumuliert Ist + Art + Referenz
    fig, ax = plt.subplots(figsize=(9, 4))

    fig.patch.set_facecolor('none')  # gesamte Figure transparent
    ax.patch.set_facecolor((1, 1, 1, 0.5))  # Achsen-Hintergrund in 50 % Weiß

    xticks = [hj for hj in df_kum_lp["Halbjahr"] if hj.endswith("H2")]
    ax.plot(df_kum_lp["Halbjahr"], df_kum_lp["Kumuliert"], marker='o', label="Gesamt kumuliert")
    if "Normalladeeinrichtung" in df_group_cum.columns:
        ax.plot(df_group_cum.index, df_group_cum["Normalladeeinrichtung"], linestyle='--', marker='x', label="Normalladeeinrichtung kumuliert")
    if "Schnellladeeinrichtung" in df_group_cum.columns:
        ax.plot(df_group_cum.index, df_group_cum["Schnellladeeinrichtung"], linestyle='--', marker='x', label="Schnellladeeinrichtung kumuliert")
    ax.axvspan("2022-H2", "2023-H2", color="orange", alpha=0.3, label="Referenzzeitraum")
    ax.set_title("Öffentliche Ladepunkte – Kumulierte Ist-Daten", color="white")
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks, rotation=90, color="white")
    ax.set_xlabel("Halbjahr", color="white")
    ax.set_ylabel("Anzahl Ladepunkte (kumuliert)", color="white")
    ax.tick_params(axis="y", colors="white")
    ax.grid(True, linestyle="--", alpha=0.5)
    plt.xticks(rotation=90)
    ax.legend(loc="best")
    st.pyplot(fig)

    # Info-Box Referenzanstieg
    start = df_kum_lp.loc[df_kum_lp["Halbjahr"]=="2022-H2","Kumuliert"].values[0]
    end   = df_kum_lp.loc[df_kum_lp["Halbjahr"]=="2023-H2","Kumuliert"].values[0]
    prozent = round((end - start) / start * 100, 2)
    delta   = int(end - start)
    st.info(f"Referenzanstieg H2-2022 bis H2-2023: +{prozent} % (+{delta:,} Ladepunkte)")

    # Prognose-Button setzt Flag
    if st.button("Prognose +41.293 LP"):
        st.session_state["prognose_aktiv"] = True

    # Anzeige und Buttons nach Klick auf Prognose
    if st.session_state["prognose_aktiv"]:
        st.markdown("""
        Artikel 'Volle Ladung Klimaschutz': 'Bis 2030 sollen in Deutschland eine Million öffentliche Ladepunkte verfügbar sein.' 
                    [Quelle: Bundesregierung](https://www.bundesregierung.de/breg-de/bundesregierung/1873986-1873986)
                    """)
        df_prog = prognose_linear_referenz(df_kum_lp, "2022-H2", "2023-H2", "2030-H2")
        fig2, ax2 = plt.subplots(figsize=(9, 4))

        fig2.patch.set_facecolor("none")  # gesamte Figure transparent
        ax2.patch.set_facecolor((1, 1, 1, 0.5))  # Achsen-Hintergrund in 50 % Weiß

        # Ist-Daten
        ax2.plot(df_kum_lp["Halbjahr"], df_kum_lp["Kumuliert"], marker='o', label="Ist")
        # Prognose
        ax2.plot(df_prog["Halbjahr"], df_prog["Kumuliert"], linestyle='-', marker='x', label="Prognose")
        # Referenz
        ax2.axvspan("2022-H2", "2023-H2", color="orange", alpha=0.3, label="Referenzzeitraum")
        ax2.axhline(1_000_000, linestyle=":", color="red", label="Ziel: 1 Mio")
        # Tausender-Format Y-Achse
        fmt = FuncFormatter(lambda x, _: f"{int(x):,}".replace(",", "."))
        ax2.yaxis.set_major_formatter(fmt)
        # X-Ticks: nur H2
        xt2 = [hj for hj in list(df_kum_lp["Halbjahr"]) + list(df_prog["Halbjahr"]) if hj.endswith("H2")]
        ax2.set_xticks(xt2)
        ax2.set_xticklabels(xt2, rotation=90, color="white")
        ax2.tick_params(axis="x", colors="white")
        ax2.set_xlabel("Halbjahr", color="white")
        ax2.set_ylabel("Anzahl Ladepunkte (kumuliert)", color="white")
        ax2.tick_params(axis="y", colors='white')
        # Grid
        ax2.grid(axis="both", which="major", linestyle="--", alpha=0.5)

        # Button "tatsächlicher Bedarf"
        if st.button("tatsächlicher Bedarf"):
            st.session_state["demand_aktiv"] = True
        # Anzeige Text und Link bei Bedarf
        if st.session_state["demand_aktiv"]:
            st.markdown(
                """
                **Tatsächlicher Bedarf**: In der Studie 'Ladeinfrastruktur nach 2025/2030' wird je nach Szenario ein
                 Bedarf von 380.000 bis 680.000 öffentlich zugänglichen Ladepunkten angegeben. [Link zur Studie](https://nationale-leitstelle.de/ladebedarf-bis-2030-neu-ermittelt/).
                """
            )
            # Zielbereich nur am rechten Rand ab 2030-H2
            xt_all = xt2  # Liste der getickten Halbjahre
            if "2030-H2" in xt_all:
                start_frac = xt_all.index("2030-H2") / (len(xt_all) - 1)
                ax2.axhspan(
                    380000,
                    680000,
                    xmin=start_frac,
                    xmax=1,
                    color="green",
                    alpha=0.2,
                    label="Zielbereich 380.000–680.000 LP"
                )
        ax2.legend(loc="best")
        ax2.set_title("Prognose öffentliche Ladepunkte (konstante Steigung)", color="white")
        ax2.set_xlabel("Halbjahr", color="white")
        ax2.set_ylabel("Anzahl Ladepunkte (kumuliert)", color="white")
        ax2.tick_params(axis='y', colors='white')
        st.pyplot(fig2)