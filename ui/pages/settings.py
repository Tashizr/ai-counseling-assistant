"""
Settings page.
"""

import streamlit as st
from config import get_settings
from ui.styles import get_custom_css


def render_settings_page() -> None:
    """Render settings."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    st.markdown(
        '<div class="main-header"><h1>⚙️ Settings</h1></div>',
        unsafe_allow_html=True,
    )

    s = get_settings()
    c1, c2 = st.columns(2)
    with c1:
        st.text_input("Provider", "Groq", disabled=True)
        st.text_input("Model", s.groq_model, disabled=True)
        st.number_input("Temp", s.temperature, disabled=True)
    with c2:
        st.text_input("Database", s.database_path, disabled=True)
        st.number_input("RAG K", s.rag_top_k, disabled=True)
        st.number_input("Max Tokens", s.max_response_tokens, disabled=True)

    st.caption("Configure via Streamlit Cloud secrets or .env")
