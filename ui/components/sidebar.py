"""
Sidebar navigation component for the Streamlit UI.
"""

import streamlit as st
from config import get_settings


def render_sidebar() -> str:
    """Render the sidebar navigation and return the selected page.

    Returns:
        Selected page name.
    """
    settings = get_settings()

    with st.sidebar:
        st.title(f"{settings.app_icon} {settings.app_title}")
        st.markdown("---")

        st.markdown(
            "**Disclaimer:** This is an AI assistant for educational "
            "purposes only. Not a replacement for professional care."
        )
        st.markdown("---")

        page = st.radio(
            "Navigation",
            ["Chat", "Mood Tracker", "Session History", "Memory Viewer",
             "Knowledge Base", "Settings", "Debug"],
            label_visibility="collapsed",
        )

        st.markdown("---")

        if settings.enable_debug:
            st.caption("Debug mode: ON")

        st.caption("Local-first | Privacy-focused")

    return page
