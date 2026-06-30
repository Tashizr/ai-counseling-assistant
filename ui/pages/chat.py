"""
Main chat interface page.
"""

import streamlit as st
from ui.components.chat_bubble import render_chat_message, render_disclaimer
from ui.styles import get_custom_css


def render_chat_page() -> None:
    """Render the main chat interface."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "engine" not in st.session_state:
        st.warning("Please initialize the application first.")
        return

    render_disclaimer()

    if not st.session_state.messages:
        st.markdown(
            """
            <div class="welcome-container">
                <div style="font-size: 3rem; margin-bottom: 1rem; opacity: 0.5;">💬</div>
                <h3>How can I help you today?</h3>
                <p>I'm here to listen. Share whatever's on your mind.</p>
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

    user_input = st.chat_input("Message...")

    if user_input:
        st.session_state.messages.append({
            "role": "user",
            "content": user_input,
        })
        render_chat_message(role="user", content=user_input)

        with st.spinner(""):
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
