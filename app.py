"""
AI Counseling Assistant — Streamlit Application Entry Point

Locally-running AI counseling assistant for education, research,
and software engineering practice only.
"""

import sys
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import streamlit as st
from config import get_settings
from logging_config import setup_logging, get_logger
from database.connection import DatabaseManager
from database.models import initialize_database
from services.safety_service import SafetyService
from services.session_manager import SessionManager
from services.conversation_engine import ConversationEngine
from rag.vector_store import VectorStore
from rag.retriever import Retriever
from rag.generator import RAGGenerator
from memory.long_term import LongTermMemory

settings = get_settings()
logger = get_logger("app")


def initialize_services() -> None:
    """Initialize all application services and store in session state."""
    if "initialized" in st.session_state:
        return

    setup_logging(
        log_level=settings.log_level,
        log_dir=settings.log_dir,
        max_size_mb=settings.max_log_size_mb,
        backup_count=settings.log_backup_count,
    )

    logger.info("Initializing AI Counseling Assistant")

    db = DatabaseManager(settings.database_path)
    initialize_database(db)
    st.session_state.db = db

    user_id = str(uuid.uuid4())
    st.session_state.user_id = user_id

    vs = VectorStore(
        persist_dir=settings.chroma_persist_dir,
        collection_name=settings.chroma_collection,
        embedding_model=settings.embedding_model,
    )
    st.session_state.vector_store = vs

    retriever = Retriever(
        vector_store=vs,
        top_k=settings.rag_top_k,
        similarity_threshold=settings.rag_similarity_threshold,
    )
    rag_generator = RAGGenerator(retriever)
    st.session_state.rag_generator = rag_generator

    ltm = LongTermMemory(db)
    st.session_state.long_term_memory = ltm

    safety_service = SafetyService()
    session_manager = SessionManager(db)

    engine = ConversationEngine(
        safety_service=safety_service,
        session_manager=session_manager,
        rag_generator=rag_generator,
        long_term_memory=ltm,
    )

    engine.start_new_session(user_id)

    st.session_state.engine = engine
    st.session_state.session_manager = session_manager
    st.session_state.safety_service = safety_service
    st.session_state.messages = []
    st.session_state.initialized = True

    logger.info("Application initialized successfully")


def main() -> None:
    """Main application function."""
    st.set_page_config(
        page_title=settings.app_title,
        page_icon=settings.app_icon,
        layout="wide",
    )

    initialize_services()

    from ui.components.sidebar import render_sidebar
    page = render_sidebar()

    if page == "Chat":
        from ui.pages.chat import render_chat_page
        render_chat_page()
    elif page == "Mood Tracker":
        from ui.pages.mood_tracker import render_mood_tracker_page
        render_mood_tracker_page()
    elif page == "Session History":
        from ui.pages.session_history import render_session_history_page
        render_session_history_page()
    elif page == "Memory Viewer":
        from ui.pages.memory_viewer import render_memory_viewer_page
        render_memory_viewer_page()
    elif page == "Knowledge Base":
        from ui.pages.knowledge_base import render_knowledge_base_page
        render_knowledge_base_page()
    elif page == "Settings":
        from ui.pages.settings import render_settings_page
        render_settings_page()
    elif page == "Debug":
        from ui.pages.debug import render_debug_page
        render_debug_page()


if __name__ == "__main__":
    main()
