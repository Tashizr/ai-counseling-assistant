"""
Debug panel for developer diagnostics.
"""

import streamlit as st
from config import get_settings
from ui.styles import get_custom_css


def render_debug_page() -> None:
    """Render the debug page."""
    settings = get_settings()

    st.markdown(get_custom_css(), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="main-header">
            <h1>🔧 Debug</h1>
            <p>System diagnostics.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not settings.enable_debug:
        st.warning("Debug mode disabled. Set ENABLE_DEBUG=true in secrets.")
        return

    col1, col2 = st.columns(2)

    with col1:
        st.success("Engine: Active") if "engine" in st.session_state else st.error("Engine: Inactive")
        st.success("Database: OK") if "db" in st.session_state else st.error("Database: Off")

    with col2:
        count = st.session_state.vector_store.count if "vector_store" in st.session_state else 0
        st.success(f"VectorStore: {count} docs") if count else st.error("VectorStore: Inactive")

    st.markdown("---")
    st.json(list(st.session_state.keys()))

    if "messages" in st.session_state:
        st.markdown(f"**Messages: {len(st.session_state.messages)}**")

    st.json({
        "model": settings.groq_model,
        "temp": settings.temperature,
        "risk": settings.risk_threshold,
    })
