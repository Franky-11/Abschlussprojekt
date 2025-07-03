import matplotlib.pyplot as plt
import numpy as np
import streamlit as st

def render_burndown_chart(width_in_inches=8):
    total_tasks = 60
    sprint_days = 21
    days = np.arange(1, sprint_days + 1)
    ideal_burndown = np.linspace(total_tasks, 0, sprint_days)
    actual_burndown = np.array([
        60, 58, 55, 52, 50, 48, 47, 45, 43, 40,
        38, 36, 34, 32, 28, 25, 20, 15, 10, 5, 2
    ])

    if len(actual_burndown) != sprint_days:
        if len(actual_burndown) > sprint_days:
            actual_burndown = actual_burndown[:sprint_days]
        else:
            actual_burndown = np.pad(actual_burndown, (0, sprint_days - len(actual_burndown)), 'edge')

    fig, ax = plt.subplots(figsize=(width_in_inches, 5))
    ax.plot(days, ideal_burndown, linestyle='--', color='gold', label='Ideale Burndown-Linie')
    ax.plot(days, actual_burndown, linestyle='-', color='darkorange', label='Tatsächliche Burndown-Linie')
    ax.set_title('📉 Burndown Chart – Projektverlauf', fontsize=16, fontweight='bold')
    ax.set_xlabel('Sprint-Tage')
    ax.set_ylabel('Verbleibende Aufgaben')
    ax.set_xlim(1, sprint_days)
    ax.set_ylim(0, total_tasks)
    ax.grid(True, linestyle=':', alpha=0.7)
    ax.legend()

    # Als Bild speichern (optional)
    fig.savefig("images/watermark/scrum_burndown_chart.png", dpi=300, bbox_inches="tight")
    st.pyplot(fig, use_container_width=False)
