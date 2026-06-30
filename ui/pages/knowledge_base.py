"""
Knowledge base page.
"""

import streamlit as st
from ui.styles import get_custom_css


def render_knowledge_base_page() -> None:
    """Render knowledge base."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    st.markdown(
        '<div class="main-header"><h1>📚 Knowledge Base</h1>'
        '<p>Educational content for RAG.</p></div>',
        unsafe_allow_html=True,
    )

    if "vector_store" not in st.session_state:
        st.info("Vector store not initialized.")
        return

    vs = st.session_state.vector_store
    c1, c2 = st.columns(2)
    c1.metric("Documents", vs.count)
    c2.metric("Collection", "counseling_knowledge")

    st.markdown("---")
    uploaded = st.file_uploader("Upload file", type=["txt", "json"])

    if uploaded:
        content = uploaded.read().decode("utf-8")
        if st.button("Add"):
            from preprocessing.cleaner import TextCleaner
            from preprocessing.chunker import SemanticChunker

            cleaned = TextCleaner().clean(content)
            if cleaned:
                chunks = SemanticChunker().chunk(cleaned, source=uploaded.name)
                vs.add_documents(
                    texts=[c.text for c in chunks],
                    metadatas=[{"source": uploaded.name} for _ in chunks],
                )
                st.success(f"Added {len(chunks)} chunks")
            else:
                st.error("Empty after cleaning")
