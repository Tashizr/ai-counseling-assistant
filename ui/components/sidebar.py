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
            """
            <div style="padding: 0.5rem 0 1rem 0; border-bottom: 1px solid #222; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 1.2rem;">🧠</span>
                    <span style="color: #e0e0e0; font-size: 0.95rem; font-weight: 600;">
                        AI Counseling
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        page = st.radio(
            "Navigate",
            ["💬 Chat", "📊 Mood Tracker", "📋 Sessions", "🧠 Memory",
             "📚 Knowledge Base", "⚙️ Settings", "🔧 Debug"],
            label_visibility="collapsed",
        )

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="padding: 0.75rem; background: #1a1111; border-radius: 0.5rem;
                        border: 1px solid #332222; font-size: 0.72rem; color: #888;
                        line-height: 1.4;">
                <span style="color: #b71c1c;">●</span>
                AI assistant — not a licensed therapist.
            </div>
            """,
            unsafe_allow_html=True,
        )

    page_map = {
        "💬 Chat": "Chat",
        "📊 Mood Tracker": "Mood Tracker",
        "📋 Sessions": "Session History",
        "🧠 Memory": "Memory Viewer",
        "📚 Knowledge Base": "Knowledge Base",
        "⚙️ Settings": "Settings",
        "🔧 Debug": "Debug",
    }
    return page_map.get(page, "Chat")
