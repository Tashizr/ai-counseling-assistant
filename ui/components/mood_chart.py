"""
Mood visualization chart component.
"""

import streamlit as st
import pandas as pd
from typing import Optional


def render_mood_chart(mood_data: list[dict]) -> None:
    """Render a mood tracking chart.

    Args:
        mood_data: List of mood entries with 'timestamp' and 'mood_score'.
    """
    if not mood_data:
        st.info("No mood data yet. Start a conversation to track your mood.")
        return

    df = pd.DataFrame(mood_data)
    if "timestamp" in df.columns and "mood_score" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.sort_values("timestamp")

        st.line_chart(
            df.set_index("timestamp")["mood_score"],
            use_container_width=True,
            height=300,
        )

        col1, col2, col3 = st.columns(3)
        with col1:
            avg_mood = df["mood_score"].mean()
            st.metric("Average", f"{avg_mood:.1f}/10")
        with col2:
            latest = df["mood_score"].iloc[-1]
            st.metric("Latest", f"{latest}/10")
        with col3:
            if len(df) > 1:
                previous = df["mood_score"].iloc[-2]
                delta = latest - previous
                st.metric("Change", f"{delta:+.1f}")
            else:
                st.metric("Sessions", f"{len(df)}")
    else:
        st.info("Mood data format is invalid.")
