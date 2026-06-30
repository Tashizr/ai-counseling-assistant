"""
Centralized configuration for AI Counseling Assistant.

Loads settings from Streamlit secrets, environment variables, or .env file.
"""

import os
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()


def _get_secret(key: str, default: str = "") -> str:
    """Read a value from Streamlit secrets or environment, falling back to default."""
    try:
        import streamlit as st
        if hasattr(st, "secrets") and key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        pass
    return os.getenv(key, default)


def _get_secret_int(key: str, default: int = 0) -> int:
    """Read an integer from Streamlit secrets or environment."""
    raw = _get_secret(key, "")
    if not raw:
        return default
    try:
        return int(raw)
    except ValueError:
        return default


def _get_secret_float(key: str, default: float = 0.0) -> float:
    """Read a float from Streamlit secrets or environment."""
    raw = _get_secret(key, "")
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        return default


def _get_secret_bool(key: str, default: bool = False) -> bool:
    """Read a boolean from Streamlit secrets or environment."""
    raw = _get_secret(key, "")
    if not raw:
        return default
    return raw.lower() in ("true", "1", "yes")


@dataclass(frozen=True)
class Settings:
    """Application configuration loaded from environment variables.

    Attributes:
        groq_api_key: API key for Groq cloud LLM.
        groq_model: Groq model name for generation.
        embedding_model: Sentence transformer model name.
        embedding_dimension: Dimension of the embedding vectors.
        chroma_persist_dir: Directory for ChromaDB persistence.
        chroma_collection: Name of the ChromaDB collection.
        database_path: Path to the SQLite database file.
        log_level: Logging verbosity level.
        log_dir: Directory for log files.
        max_log_size_mb: Maximum log file size in megabytes.
        log_backup_count: Number of rotated log files to keep.
        max_context_messages: Maximum messages to include in LLM context.
        max_response_tokens: Maximum tokens in LLM response.
        temperature: Sampling temperature for LLM generation.
        top_p: Top-p sampling parameter for LLM generation.
        risk_threshold: Minimum risk level to trigger safety responses.
        enable_safety_filters: Whether to enable post-generation safety checks.
        rag_top_k: Number of RAG passages to retrieve.
        rag_similarity_threshold: Minimum similarity score for RAG results.
        short_term_max_messages: Maximum messages kept in short-term memory.
        long_term_summary_interval: Message count between long-term summaries.
        enable_debug: Whether debug mode is active.
        app_title: Application title displayed in the UI.
        app_icon: Emoji icon for the application.
        theme_primary: Primary theme color for the UI.
    """

    # LLM Provider
    groq_api_key: str = field(default_factory=lambda: _get_secret("GROQ_API_KEY", ""))
    groq_model: str = field(default_factory=lambda: _get_secret("GROQ_MODEL", "llama-3.3-70b-versatile"))

    # Embeddings
    embedding_model: str = field(default_factory=lambda: _get_secret("EMBEDDING_MODEL", "all-MiniLM-L6-v2"))
    embedding_dimension: int = field(default_factory=lambda: _get_secret_int("EMBEDDING_DIMENSION", 384))

    # ChromaDB
    chroma_persist_dir: str = field(default_factory=lambda: _get_secret("CHROMA_PERSIST_DIR", "./chroma_db"))
    chroma_collection: str = field(default_factory=lambda: _get_secret("CHROMA_COLLECTION", "counseling_knowledge_v2"))

    # Database
    database_path: str = field(default_factory=lambda: _get_secret("DATABASE_PATH", "./data/counseling.db"))

    # Logging
    log_level: str = field(default_factory=lambda: _get_secret("LOG_LEVEL", "INFO"))
    log_dir: str = field(default_factory=lambda: _get_secret("LOG_DIR", "./logs"))
    max_log_size_mb: int = field(default_factory=lambda: _get_secret_int("MAX_LOG_SIZE_MB", 10))
    log_backup_count: int = field(default_factory=lambda: _get_secret_int("LOG_BACKUP_COUNT", 5))

    # Conversation
    max_context_messages: int = field(default_factory=lambda: _get_secret_int("MAX_CONTEXT_MESSAGES", 20))
    max_response_tokens: int = field(default_factory=lambda: _get_secret_int("MAX_RESPONSE_TOKENS", 256))
    temperature: float = field(default_factory=lambda: _get_secret_float("TEMPERATURE", 0.7))
    top_p: float = field(default_factory=lambda: _get_secret_float("TOP_P", 0.9))

    # Safety
    risk_threshold: str = field(default_factory=lambda: _get_secret("RISK_THRESHOLD", "moderate"))
    enable_safety_filters: bool = field(default_factory=lambda: _get_secret_bool("ENABLE_SAFETY_FILTERS", True))

    # RAG
    rag_top_k: int = field(default_factory=lambda: _get_secret_int("RAG_TOP_K", 5))
    rag_similarity_threshold: float = field(default_factory=lambda: _get_secret_float("RAG_SIMILARITY_THRESHOLD", 0.3))

    # Memory
    short_term_max_messages: int = field(default_factory=lambda: _get_secret_int("SHORT_TERM_MAX_MESSAGES", 50))
    long_term_summary_interval: int = field(default_factory=lambda: _get_secret_int("LONG_TERM_SUMMARY_INTERVAL", 10))

    # UI
    enable_debug: bool = field(default_factory=lambda: _get_secret_bool("ENABLE_DEBUG", False))
    app_title: str = field(default_factory=lambda: _get_secret("APP_TITLE", "AI Counseling Assistant"))
    app_icon: str = field(default_factory=lambda: _get_secret("APP_ICON", "🧠"))
    theme_primary: str = field(default_factory=lambda: _get_secret("THEME_PRIMARY", "#4A90D9"))

    def __post_init__(self) -> None:
        """Validate configuration values after initialization."""
        if not 0.0 <= self.temperature <= 2.0:
            raise ValueError(
                f"temperature must be between 0.0 and 2.0, got {self.temperature}"
            )
        if not 0.0 <= self.top_p <= 1.0:
            raise ValueError(
                f"top_p must be between 0.0 and 1.0, got {self.top_p}"
            )
        if self.risk_threshold not in _VALID_RISK_LEVELS:
            raise ValueError(
                f"risk_threshold must be one of {_VALID_RISK_LEVELS}, got '{self.risk_threshold}'"
            )
        if self.log_level not in _VALID_LOG_LEVELS:
            raise ValueError(
                f"log_level must be one of {_VALID_LOG_LEVELS}, got '{self.log_level}'"
            )


settings = Settings()


def get_settings() -> Settings:
    """Return the global settings instance.

    Returns:
        The application settings singleton.
    """
    return settings
