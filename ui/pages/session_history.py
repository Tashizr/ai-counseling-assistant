"""
Session history page for viewing past conversations.
"""

import streamlit as st
from ui.styles import get_custom_css


def render_session_history_page() -> None:
    """Render the session history page."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="main-header">
            <h1>📋 Sessions</h1>
            <p>Review your past conversations.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "session_manager" not in st.session_state:
        st.warning("Please initialize the application first.")
        return

    session_mgr = st.session_state.session_manager
    user_id = st.session_state.get("user_id", "default_user")

    conversations = session_mgr.get_recent_conversations(user_id, limit=20)

    if not conversations:
        st.info("No past conversations yet.")
        return

    for conv in conversations:
        with st.expander(
            f"{conv['started_at'][:10]} | Risk: {conv.get('risk_level_max', 'low')}"
        ):
            if conv.get("summary"):
                st.write(conv["summary"])
            else:
                st.caption("No summary available")

            col1, col2 = st.columns(2)
            with col1:
                if conv.get("mood_start"):
                    st.metric("Start", f"{conv['mood_start']}/10")
            with col2:
                if conv.get("mood_end"):
                    st.metric("End", f"{conv['mood_end']}/10")

            st.caption(f"Started: {conv['started_at']}")
