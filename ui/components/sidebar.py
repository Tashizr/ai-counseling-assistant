"""
Sidebar navigation component.
"""

import streamlit as st


def render_sidebar() -> str:
    """Render sidebar and return selected page."""
    with st.sidebar:
        st.markdown(
            '<div style="padding: 0 0 0.75rem 0; border-bottom: 1px solid #1a1a1a;">'
            '<span style="color:#e0e0e0;font-size:0.9rem;font-weight:600;">🧠 AI Counseling</span>'
            '</div>',
            unsafe_allow_html=True,
        )

        page = st.radio(
            "Nav",
            ["💬 Chat", "📊 Mood", "📋 Sessions", "🧠 Memory", "📚 KB", "⚙️ Settings"],
            label_visibility="collapsed",
        )

        st.markdown(
            '<div style="position:fixed;bottom:1rem;left:1rem;right:1rem;'
            'font-size:0.65rem;color:#444;text-align:center;">'
            'AI assistant — not a licensed therapist</div>',
            unsafe_allow_html=True,
        )

    return {
        "💬 Chat": "Chat",
        "📊 Mood": "Mood Tracker",
        "📋 Sessions": "Session History",
        "🧠 Memory": "Memory Viewer",
        "📚 KB": "Knowledge Base",
        "⚙️ Settings": "Settings",
    }.get(page, "Chat")
