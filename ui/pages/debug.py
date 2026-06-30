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
            <h1>🔧 Debug Panel</h1>
            <p>Developer diagnostics and system state.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not settings.enable_debug:
        st.warning(
            "Debug mode is disabled. Set ENABLE_DEBUG=true in secrets to enable."
        )
        return

    st.markdown("**System Status**")

    col1, col2 = st.columns(2)

    with col1:
        if "engine" in st.session_state:
            st.success("ConversationEngine: Active")
        else:
            st.error("ConversationEngine: Inactive")

        if "db" in st.session_state:
            st.success("Database: Connected")
        else:
            st.error("Database: Disconnected")

    with col2:
        if "vector_store" in st.session_state:
            st.success(f"VectorStore: {st.session_state.vector_store.count} docs")
        else:
            st.error("VectorStore: Inactive")

    st.markdown("---")
    st.markdown("**Session State**")
    st.json(list(st.session_state.keys()))

    if "messages" in st.session_state:
        st.markdown(f"**Messages: {len(st.session_state.messages)}**")
        for msg in st.session_state.messages[-5:]:
            st.text(f"[{msg['role']}] {msg['content'][:100]}...")

    st.markdown("---")
    st.markdown("**Configuration**")
    st.json({
        "groq_model": settings.groq_model,
        "temperature": settings.temperature,
        "rag_top_k": settings.rag_top_k,
        "risk_threshold": settings.risk_threshold,
    })
