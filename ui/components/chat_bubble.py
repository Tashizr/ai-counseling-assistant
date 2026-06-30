"""
Chat bubble component for rendering messages.
"""

import streamlit as st
from typing import Optional


def render_chat_message(
    role: str,
    content: str,
    emotion: Optional[str] = None,
    risk_level: Optional[str] = None,
) -> None:
    """Render a single chat message."""
    if role == "user":
        with st.chat_message("user", avatar="🧑"):
            st.markdown(content)
    else:
        with st.chat_message("assistant", avatar="🔴"):
            st.markdown(content)
            if risk_level and risk_level != "low":
                st.markdown(
                    f'<span class="risk-badge risk-{risk_level}">{risk_level.upper()}</span>',
                    unsafe_allow_html=True,
                )


def render_disclaimer() -> None:
    """Render the identity disclaimer."""
    st.markdown(
        '<div class="disclaimer-box">'
        "🤖 AI assistant — not a licensed therapist. I can't diagnose or provide emergency care."
        "</div>",
        unsafe_allow_html=True,
    )
