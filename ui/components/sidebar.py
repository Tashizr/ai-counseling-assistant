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
        st.markdown(
            f"""
            <div style="text-align: center; padding: 1rem 0;">
                <div style="font-size: 2.5rem;">🧠</div>
                <h2 style="color: white; margin: 0; font-size: 1.1rem; font-weight: 600;">
                    AI Counseling
                </h2>
                <p style="color: #888; font-size: 0.75rem; margin: 0.25rem 0 0 0;">
                    Safe space for support
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")

        page = st.radio(
            "Navigate",
            ["💬 Chat", "📊 Mood Tracker", "📋 Session History", "🧠 Memory",
             "📚 Knowledge Base", "⚙️ Settings", "🔧 Debug"],
            label_visibility="collapsed",
        )

        st.markdown("---")

        st.markdown(
            """
            <div style="padding: 0.5rem; font-size: 0.75rem; color: #666; line-height: 1.4;">
                <strong style="color: #999;">Reminder</strong><br>
                I'm an AI assistant for educational purposes. Not a replacement for professional care.
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown(
            '<div style="text-align: center; font-size: 0.7rem; color: #555;">'
            'Local-first | Privacy-focused'
            '</div>',
            unsafe_allow_html=True,
        )

    # Clean page name for routing
    page_map = {
        "💬 Chat": "Chat",
        "📊 Mood Tracker": "Mood Tracker",
        "📋 Session History": "Session History",
        "🧠 Memory": "Memory Viewer",
        "📚 Knowledge Base": "Knowledge Base",
        "⚙️ Settings": "Settings",
        "🔧 Debug": "Debug",
    }
    return page_map.get(page, "Chat")
