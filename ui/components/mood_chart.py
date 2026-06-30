"""
Mood visualization chart component.
"""

import streamlit as st
import pandas as pd


def render_mood_chart(mood_data: list[dict]) -> None:
    """Render mood tracking chart."""
    if not mood_data:
        st.info("No mood data yet.")
        return

    df = pd.DataFrame(mood_data)
    if "timestamp" in df.columns and "mood_score" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")

        st.line_chart(
            df.set_index("timestamp")["mood_score"],
            use_container_width=True,
            height=200,
        )

        cols = st.columns(3)
        cols[0].metric("Avg", f"{df['mood_score'].mean():.1f}")
        cols[1].metric("Latest", f"{df['mood_score'].iloc[-1]}")
        if len(df) > 1:
            d = df["mood_score"].iloc[-1] - df["mood_score"].iloc[-2]
            cols[2].metric("Δ", f"{d:+.0f}")
