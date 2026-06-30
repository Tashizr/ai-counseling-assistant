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
            <p>View and manage your application configuration.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    settings = get_settings()

    st.markdown("**Current Configuration**")

    col1, col2 = st.columns(2)

    with col1:
        st.text_input("LLM Provider", value="Groq", disabled=True)
        st.text_input("Model", value=settings.groq_model, disabled=True)
        st.text_input("Embedding Model", value=settings.embedding_model, disabled=True)
        st.number_input("Temperature", value=settings.temperature, disabled=True)
        st.number_input("Top P", value=settings.top_p, disabled=True)

    with col2:
        st.text_input("Database Path", value=settings.database_path, disabled=True)
        st.text_input("ChromaDB Dir", value=settings.chroma_persist_dir, disabled=True)
        st.text_input("Log Level", value=settings.log_level, disabled=True)
        st.number_input("Max Context Messages", value=settings.max_context_messages, disabled=True)
        st.number_input("RAG Top K", value=settings.rag_top_k, disabled=True)

    st.markdown("---")

    st.markdown(
        """
        **About**
        This AI Counseling Assistant is designed for **education, research, "
        "and software engineering practice only**. It is not a replacement "
        "for licensed mental health professionals.
        """
    )

    st.markdown("---")
    st.caption("Configuration is managed via Streamlit Cloud secrets or .env file.")
