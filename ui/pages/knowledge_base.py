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
            <p>Educational content used for retrieval-augmented generation.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "vector_store" in st.session_state:
        vs = st.session_state.vector_store

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Documents", vs.count)
        with col2:
            st.metric("Collection", "counseling_knowledge")

        st.markdown("---")

        st.markdown("**Add Documents**")
        uploaded_file = st.file_uploader(
            "Upload a text or JSON file",
            type=["txt", "json"],
            help="Upload educational content to add to the knowledge base",
        )

        if uploaded_file:
            content = uploaded_file.read().decode("utf-8")
            if st.button("Add to Knowledge Base"):
                from preprocessing.cleaner import TextCleaner
                from preprocessing.chunker import SemanticChunker

                cleaner = TextCleaner()
                chunker = SemanticChunker()

                cleaned = cleaner.clean(content)
                if cleaned:
                    chunks = chunker.chunk(
                        cleaned,
                        source=uploaded_file.name,
                    )
                    texts = [c.text for c in chunks]
                    vs.add_documents(
                        texts=texts,
                        metadatas=[{"source": uploaded_file.name} for _ in texts],
                    )
                    st.success(f"Added {len(texts)} chunks from {uploaded_file.name}")
                else:
                    st.error("File content was empty after cleaning")
    else:
        st.info("Vector store not initialized. Please run the application first.")

    st.markdown("---")
    st.markdown(
        """
        **Supported Topics**
        - CBT & DBT
        - Crisis Intervention
        - Motivational Interviewing
        - Emotional Intelligence
        - Active Listening
        - Positive Psychology
        - Mindfulness
        """
    )
