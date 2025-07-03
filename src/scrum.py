# scrum.py – Abschlussprojekt / Scrum-Dokumentation
# Diese Datei wird durch home.py dynamisch geladen
# -------------------------------------------------
# Erwartete Dateien (relativ zum Start-Verzeichnis):
#   images/watermark/scrum_timeline.png
#   images/watermark/trello_summary.png
#   images/watermark/scrum_burndown_chart.png  (wird beim ersten Lauf erzeugt)
# -------------------------------------------------

import os
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from render_burndown_chart import render_burndown_chart
from datetime import datetime
from watermarks import set_watermark


# ─────────────────────────────────────────────────────────────
# Streamlit-Code als Funktion kapseln
# ─────────────────────────────────────────────────────────────

def run():
    # ───────────────── Streamlit-Setup ─────────────────
    set_watermark("images/watermark/chargingpoints_pic.png")

    st.title("🧭 Scrum Übersicht – Abschlussprojekt")

    # ───────────────── Einleitung ──────────────────────
    st.markdown(
        """
Willkommen auf der Scrum-Seite unseres Abschlussprojekts.

Wir nutzen **Scrum**, um unser kleines Team (3 Personen) effizient zu organisieren,
Rollen klar zu verteilen und iterativ Mehrwert zu schaffen.

### 📚 Hintergrundwissen – Scrum in kleinen Teams
> „Scrum hilft kleinen Teams, effizient und flexibel zu arbeiten …“  
> — *Scrum Guide, Ken Schwaber & Jeff Sutherland*

> Laut [Atlassian](https://www.atlassian.com/agile/scrum) sind Teams von 3 – 9 Mitgliedern
> am produktivsten, da enge Zusammenarbeit und schnelle Feedback-Loops gefördert werden.

**Unsere Umsetzung**

- tägliche **Daily Scrums** via Google Meet  
- drei **Sprints à 1 Woche** mit klaren Zielen  
- **Sprint Reviews** gemeinsam mit den Coaches  
- Aufgabenkoordination über **Trello**

---
"""
    )

    # ───────────────── Meeting-Liste ───────────────────
    st.markdown(
        """
### 📅 Meetings & Scrum-Events  
Insgesamt führten wir **31 dokumentierte Meetings** durch (Daily Scrums, Plannings, Reviews …):

```text
1. Sprint Planning #0 (29.05.)
2. Daily Scrum (31.05.)
3. Backlog Grooming (01.06.)
…
31. Retrospektive & Projektabschluss (03.07.)
"""
    )

    raw_data = [
        ["2025-05-22", "12:59", "15:15", "Gruppeneinteilung", "Other"],
        ["2025-05-26", "12:01", "13:15", "Projekttreffen, Einladung per Kalender", "Other"],
        ["2025-05-30", "10:00", "11:29", "Projekttreffen", "Other"],
        ["2025-06-01", "10:58", "13:00", "Trello Board + Meeting", "Backlog Refinement"],
        ["2025-06-02", "11:00", "12:00", "Projekt Backlog", "Backlog Refinement"],
        ["2025-06-03", "11:09", "13:09", "Backlog & Sprint Planning", "Sprint Planning"],
        ["2025-06-05", "11:00", "11:45", "Präsentationen und Fachgespräch", "Review"],
        ["2025-06-07", "10:00", "11:00", "Recherchesitzung, KI, Gemini-Link", "Other"],
        ["2025-06-08", "10:30", "11:30", "Meeting", "Daily Scrum"],
        ["2025-06-09", "10:30", "11:30", "Fragen und Vorbereitung für DSI", "Other"],
        ["2025-06-11", "10:32", "12:32", "Meeting", "Daily Scrum"],
        ["2025-06-13", "12:15", "13:15", "Abschlussmeeting", "Sprint Review"],
        ["2025-06-16", "21:00", "22:00", "Backlog aktualisieren", "Backlog Refinement"],
        ["2025-06-17", "15:15", "23:59", "Projektmeeting", "Other"],
        ["2025-06-20", "11:00", "13:00", "Abschlussprojekt", "Sprint Review"],
        ["2025-06-22", "12:00", "14:00", "Abschlussprojekt", "Sprint Review"],
        ["2025-06-23", "14:00", "15:00", "Projektbesprechung", "Review"],
        ["2025-06-24", "11:30", "18:30", "Projektmeeting", "Other"],
        ["2025-06-25", "20:00", "23:50", "Projektbesprechung", "Other"],
        ["2025-06-26", "21:00", "22:00", "DSI Abschlussprojekt", "Other"],
        ["2025-06-28", "12:00", "15:00", "Meeting", "Daily Scrum"],
        ["2025-06-29", "15:30", "17:30", "Meeting", "Daily Scrum"],
        ["2025-06-30", "14:00", "17:00", "Abschlussmeeting", "Sprint Review"],
        ["2025-07-01", "15:00", "18:00", "Abschlussmeeting", "Sprint Review"],
        ["2025-07-02", "12:15", "23:30", "Nachentwicklung", "Other"],
        ["2025-07-03", "09:30", "21:00", "Feinschliff & Übung", "Other"]
    ]

    data = []
    for entry in raw_data:
        date_str, start_str, end_str, event, phase = entry
        start_dt = datetime.strptime(f"{date_str} {start_str}", "%Y-%m-%d %H:%M")
        # Handle possible next day end time (e.g. 23:30 to 00:30)
        end_dt = datetime.strptime(f"{date_str} {end_str}", "%Y-%m-%d %H:%M")
        if end_dt <= start_dt:
            end_dt += pd.Timedelta(days=1)
        duration = int((end_dt - start_dt).total_seconds() / 60)
        Zeitraum = f"{start_str}–{end_str}"
        data.append([date_str, start_str, end_str, duration, event, phase, Zeitraum])

    total_minutes = sum([entry[3] for entry in data])
    st.metric("⏱ Gesamtzeit aller Meetings", f"{total_minutes / 60:.1f} Stunden")
    st.metric("👥 Gesamtzeit nach Mannstunden", f"{total_minutes * 3 / 60:.1f} Stunden")

    df = pd.DataFrame(
        data,
        columns=["Datum", "Start", "Ende", "Dauer (Minuten)", "Event", "Scrum-Phase", "Zeitraum"],
    )

    # Gruppieren nach Datum mit Aggregation der Zeiträume und Events mit Zeilenumbruch
    df_grouped = df.groupby("Datum").agg(
        Zeitraum=("Zeitraum", lambda x: "\n".join(x)),
        Event=("Event", lambda x: "\n".join(x))
    ).reset_index()

    # ───────── Zeitverteilung ─────────
    with st.expander("⏱ Meeting-Übersicht nach Datum & Zeit"):
        st.markdown("### ⏱ Meeting-Übersicht nach Datum & Zeit")

        df["Datum_fmt"] = pd.to_datetime(df["Datum"])
        # Berechnung Minuten nach Mitternacht für Start und Ende
        df["Startzeit_min"] = df["Start"].apply(lambda t: int(t.split(":")[0]) * 60 + int(t.split(":")[1]))
        df["Endezeit_min"] = df["Ende"].apply(lambda t: int(t.split(":")[0]) * 60 + int(t.split(":")[1]))
        # Wenn Endezeit kleiner als Startzeit, dann Endezeit + 24*60 Minuten
        df.loc[df["Endezeit_min"] <= df["Startzeit_min"], "Endezeit_min"] += 24 * 60

        import matplotlib.dates as mdates
        fig, ax = plt.subplots(figsize=(10, 6))
        for _, row in df.iterrows():
            ax.plot([row["Datum_fmt"], row["Datum_fmt"]], [row["Startzeit_min"], row["Endezeit_min"]], marker='o')
        ax.set_xlabel("Datum")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%d.%m"))
        ax.set_ylim(0, 1440)
        ax.set_yticks(range(0, 1441, 60))
        ax.set_yticklabels([f"{h}:00" for h in range(25)])
        ax.set_ylabel("Tageszeit (Minuten nach Mitternacht)")
        ax.set_title("Meetings nach Datum und Uhrzeit")
        ax.grid(True)

        st.pyplot(fig)

    # ───────── Projektteam─────────

    with st.expander("Projektteam"):
        st.markdown(
            """
    Dieses Projekt wurde im Rahmen unserer Data-Science-Weiterbildung erstellt.  

    Data Science Institute by Fabian Rappert / DSI Education GmbH, Berlin  
    <https://data-science-institute.de>

    **Projektteam & Fokus**  
    * **Philipp Schauer** – Ladeinfrastruktur  
    * **Thomas Baur** – Projektmanagement, Stromerzeugung  
    * **Frank Schulnies** – Fahrzeugmarkt  

    Unser Ziel war es, ein nützliches und intuitives Tool zu entwickeln, das einen Beitrag zur Diskussion um die Zukunft der E-Mobilität leistet.
    """
        )

    # ───────── Projektbeschreibung ─────────

    with st.expander("📝 Projektbeschreibung"):
        st.markdown(
            """
Projektidee: Potenzialanalyse Elektromobilität Deutschland

Ein Podcast aus unseren ersten gesammelten Studien und Informationen, vermittelt einen ersten Eindruck unserer unserer ursprünglichen Fragen, die sich jedoch im Laufe des Projektes durch iterieren im Scrum verfeinerten.

Teilbereiche: Fahrzeugmarkt, Ladeinfrastruktur, Stromerzeugung,
gesellschaftliche Akzeptanz

Tools & Daten: Python, Streamlit, Plotly, SMARD, BNetzA, KBA, OpenChargeMap, Trello, GitHub

Rollen:
    •    Thomas Baur – Scrum Master
    •    Frank Schulnies – Product Owner
    •    Philipp Schauer – Developer Lead

Abgabe & Präsentation: 04.07.2025 (30 min Vortrag + 10 min Q&A)
"""
        )
        st.audio("audio/Ursprungsfragestellung.wav")
        
    # ───────── Timeline-Bild ────────────

    # ───────── Burndown-Chart ───────────
    with st.expander("📉 Burndown Chart"):
        st.markdown("### 📉 Burndown Chart")
        render_burndown_chart(width_in_inches=6)

    # ───────── Meeting-Tabelle ───────────

    with st.expander("📋 Alle Meetings anzeigen"):
        st.dataframe(df_grouped, use_container_width=True)

    # ───────── Trello-Snapshot ───────────
    with st.expander("📌 Trello Snapshot"):
        st.markdown("### 📌 Trello Snapshot")
        st.markdown("Trello diente uns zur Sprintplanung, Aufgabenverteilung und Dokumentation des Fortschritts.")
        st.image(
            "images/watermark/trello_summary.png",
            caption="Trello Board – Stand Abschlussphase",
            width=600,
        )

    # ───────── Footer ───────────

    st.markdown("---")
    st.success("🚀 Kleine Teams + Scrum ⇒ transparent, fokussiert und iterativ erfolgreich!")
