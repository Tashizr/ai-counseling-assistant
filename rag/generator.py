"""
RAG generator — orchestrates retrieval and response generation.

Combines retrieved context with the LLM to generate informed responses.
"""

import logging
from typing import Optional

from rag.retriever import Retriever

logger = logging.getLogger(__name__)


class RAGGenerator:
    """Orchestrates RAG-based response generation.

    Retrieves relevant context and prepares it for the conversation engine
    to use when generating responses.
    """

    def __init__(self, retriever: Retriever) -> None:
        """Initialize the RAG generator.

        Args:
            retriever: The Retriever instance for knowledge lookup.
        """
        self._retriever = retriever
        logger.debug("RAGGenerator initialized")

    def get_context(self, query: str) -> str:
        """Retrieve and format context for a user query.

        Args:
            query: The user's message or query.

        Returns:
            Formatted context string for the system prompt.
        """
        passages = self._retriever.retrieve(query)
        return self._retriever.format_for_prompt(passages)

    def get_context_with_metadata(self, query: str) -> dict:
        """Retrieve context with full metadata.

        Args:
            query: The user's message or query.

        Returns:
            Dict with 'context' string and 'passages' list.
        """
        passages = self._retriever.retrieve(query)
        return {
            "context": self._retriever.format_for_prompt(passages),
            "passages": passages,
            "count": len(passages),
        }
