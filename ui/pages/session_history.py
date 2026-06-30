"""
Session history page.
"""

import streamlit as st
from ui.styles import get_custom_css


def render_session_history_page() -> None:
    """Render session history."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    st.markdown(
        '<div class="main-header"><h1>📋 Sessions</h1>'
        '<p>Past conversations.</p></div>',
        unsafe_allow_html=True,
    )

    if "session_manager" not in st.session_state:
        st.warning("Initialize the application first.")
        return

    user_id = st.session_state.get("user_id", "default")
    convs = st.session_state.session_manager.get_recent_conversations(user_id, 20)

    if not convs:
        st.info("No past conversations yet.")
        return

    for c in convs:
        with st.expander(f"{c['started_at'][:10]} — {c.get('risk_level_max', 'low')}"):
            if c.get("summary"):
                st.write(c["summary"])
            cols = st.columns(2)
            if c.get("mood_start"):
                cols[0].metric("Start", f"{c['mood_start']}/10")
            if c.get("mood_end"):
                cols[1].metric("End", f"{c['mood_end']}/10")
            st.caption(c["started_at"])
