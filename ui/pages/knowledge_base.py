"""
Knowledge base management and statistics page.
"""

import streamlit as st
from ui.styles import get_custom_css


def render_knowledge_base_page() -> None:
    """Render the knowledge base page."""
    st.markdown(get_custom_css(), unsafe_allow_html=True)

    st.markdown(
        """
        <div class="main-header">
            <h1>📚 Knowledge Base</h1>
            <p>Educational content for retrieval-augmented generation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "vector_store" in st.session_state:
        vs = st.session_state.vector_store

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Documents", vs.count)
        with col2:
            st.metric("Collection", "counseling_knowledge")

        st.markdown("---")

        uploaded_file = st.file_uploader("Upload file", type=["txt", "json"])

        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
            if st.button("Add to Knowledge Base"):
                from preprocessing.cleaner import TextCleaner
                from preprocessing.chunker import SemanticChunker

                cleaner = TextCleaner()
                chunker = SemanticChunker()

                cleaned = cleaner.clean(content)
                if cleaned:
                    chunks = chunker.chunk(cleaned, source=uploaded_file.name)
                    texts = [c.text for c in chunks]
                    vs.add_documents(
                        texts=texts,
                        metadatas=[{"source": uploaded_file.name} for _ in texts],
                    )
                    st.success(f"Added {len(texts)} chunks")
                else:
                    st.error("File was empty after cleaning")
    else:
        st.info("Vector store not initialized.")

    st.markdown("---")
    st.markdown("**Topics:** CBT, DBT, Crisis Intervention, MI, EI, Active Listening, Mindfulness")
