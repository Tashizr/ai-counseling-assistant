"""
Main chat interface page.
"""

import streamlit as st
from ui.components.chat_bubble import render_chat_message, render_disclaimer
from ui.styles import get_custom_css


def render_chat_page() -> None:
    """Render the main chat interface."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    render_disclaimer()

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "engine" not in st.session_state:
        st.warning("Please initialize the application first.")
        return

    for msg in st.session_state.messages:
        render_chat_message(
            role=msg["role"],
            content=msg["content"],
            emotion=msg.get("emotion"),
            risk_level=msg.get("risk_level"),
        )

    user_input = st.chat_input("Type your message here...")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
        })
        render_chat_message(role="user", content=user_input)

        with st.spinner("Thinking..."):
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
