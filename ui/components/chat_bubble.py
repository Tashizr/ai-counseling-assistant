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
    """Render a single chat message bubble.

    Args:
        role: 'user' or 'assistant'.
        content: Message content.
        emotion: Optional detected emotion.
        risk_level: Optional risk level.
    """
    if role == "user":
        with st.chat_message("user", avatar="🧑"):
            st.markdown(content)
    else:
        with st.chat_message("assistant", avatar="🔴"):
            st.markdown(content)
            if risk_level and risk_level != "low":
                risk_class = f"risk-{risk_level}"
                st.markdown(
                    f'<span class="risk-badge {risk_class}">{risk_level.upper()}</span>',
                    unsafe_allow_html=True,
                )


def render_crisis_banner(resources: str) -> None:
    """Render a crisis resources banner.

    Args:
        resources: Formatted crisis resource string.
    """
    st.markdown(
        f'<div class="crisis-box">'
        f"<strong>Important:</strong> If you're in crisis, please reach out for help:<br>"
        f"{resources}"
        f"</div>",
        unsafe_allow_html=True,
    )


def render_disclaimer() -> None:
    """Render the identity disclaimer banner."""
    st.markdown(
        '<div class="disclaimer-box">'
        "🤖 AI assistant — not a licensed therapist. I can't diagnose, treat, or provide emergency care."
        "</div>",
        unsafe_allow_html=True,
    )
