"""
Mood tracker page.
"""

import streamlit as st
from ui.styles import get_custom_css
from ui.components.mood_chart import render_mood_chart


def render_mood_tracker_page() -> None:
    """Render the mood tracker page."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    st.markdown(
        '<div class="main-header"><h1>📊 Mood</h1>'
        '<p>Track your emotional well-being over time.</p></div>',
        unsafe_allow_html=True,
    )

    if "engine" not in st.session_state:
        st.warning("Initialize the application first.")
        return

    mood = st.session_state.engine.get_mood_score()
    if mood:
        st.info(f"Current session mood: {mood}/10")

    if "db" in st.session_state and "user_id" in st.session_state:
        data = st.session_state.db.fetch_all(
            "SELECT mood_score, emotions, timestamp FROM mood_entries "
            "WHERE user_id = ? ORDER BY timestamp DESC LIMIT 30",
            (st.session_state.user_id,),
        )
        render_mood_chart(data)
    else:
        st.info("No mood data yet.")
