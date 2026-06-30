"""
Debug panel for developer diagnostics.
"""

import streamlit as st
from config import get_settings


def render_debug_page() -> None:
    """Render the debug page."""
    settings = get_settings()

    if not settings.enable_debug:
        st.warning(
            "Debug mode is disabled. Set ENABLE_DEBUG=true in .env to enable."
        )
        return

    st.title("Debug Panel")

    st.markdown("**System State**")

    if "engine" in st.session_state:
        st.success("ConversationEngine: Initialized")
    else:
        st.error("ConversationEngine: Not initialized")

    if "db" in st.session_state:
        st.success("Database: Connected")
    else:
        st.error("Database: Not connected")

    if "vector_store" in st.session_state:
        st.success(f"VectorStore: {st.session_state.vector_store.count} documents")
    else:
        st.error("VectorStore: Not initialized")

    st.markdown("---")
    st.markdown("**Session State Keys**")
    st.json(list(st.session_state.keys()))

    if "messages" in st.session_state:
        st.markdown("---")
        st.markdown(f"**Messages: {len(st.session_state.messages)}**")
        for i, msg in enumerate(st.session_state.messages[-5:]):
            st.text(f"[{msg['role']}] {msg['content'][:100]}...")

    st.markdown("---")
    st.markdown("**Configuration**")
    st.json({
        "ollama_model": settings.ollama_model,
        "temperature": settings.temperature,
        "rag_top_k": settings.rag_top_k,
        "risk_threshold": settings.risk_threshold,
        "short_term_max_messages": settings.short_term_max_messages,
    })
