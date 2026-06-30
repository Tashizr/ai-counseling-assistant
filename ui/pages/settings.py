"""
Settings page for application configuration.
"""

import streamlit as st
from config import get_settings
from ui.styles import get_custom_css


def render_settings_page() -> None:
    """Render the settings page."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="main-header">
            <h1>⚙️ Settings</h1>
            <p>Application configuration.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    settings = get_settings()

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("LLM Provider", value="Groq", disabled=True)
        st.text_input("Model", value=settings.groq_model, disabled=True)
        st.text_input("Embedding", value=settings.embedding_model, disabled=True)
        st.number_input("Temperature", value=settings.temperature, disabled=True)

    with col2:
        st.text_input("Database", value=settings.database_path, disabled=True)
        st.text_input("ChromaDB", value=settings.chroma_persist_dir, disabled=True)
        st.number_input("RAG Top K", value=settings.rag_top_k, disabled=True)
        st.number_input("Max Tokens", value=settings.max_response_tokens, disabled=True)

    st.markdown("---")
    st.caption("Configure via Streamlit Cloud secrets or .env file.")
