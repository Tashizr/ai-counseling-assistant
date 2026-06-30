"""
Main chat interface page.
"""

import streamlit as st
from ui.components.chat_bubble import render_chat_message, render_disclaimer
from ui.styles import get_custom_css


def render_chat_page() -> None:
    """Render the main chat interface."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="main-header">
            <h1>💬 Let's Talk</h1>
            <p>A safe space to share what's on your mind. I'm here to listen.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_disclaimer()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "engine" not in st.session_state:
        st.warning("Please initialize the application first.")
        return

    if not st.session_state.messages:
        st.markdown(
            """
            <div style="text-align: center; padding: 3rem 1rem; color: #888;">
                <div style="font-size: 3rem; margin-bottom: 1rem;">🫂</div>
                <h3 style="color: #555; font-weight: 500;">How are you feeling today?</h3>
                <p style="font-size: 0.9rem;">Type a message below to start our conversation.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    for msg in st.session_state.messages:
        render_chat_message(
            role=msg["role"],
            content=msg["content"],
            emotion=msg.get("emotion"),
            risk_level=msg.get("risk_level"),
        )

    user_input = st.chat_input("Share what's on your mind...")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
        })
        render_chat_message(role="user", content=user_input)

        with st.spinner("Listening..."):
            result = st.session_state.engine.process_message(user_input)

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["response"],
            "emotion": result.get("emotion"),
            "risk_level": result.get("risk_level"),
        })

        render_chat_message(
            role="assistant",
            content=result["response"],
            emotion=result.get("emotion"),
            risk_level=result.get("risk_level"),
        )
