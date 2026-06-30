"""
RAG retriever — finds relevant knowledge passages for user queries.

Combines vector similarity search with relevance filtering.
"""

import logging
from dataclasses import dataclass, field
from typing import Optional

from rag.vector_store import VectorStore

logger = logging.getLogger(__name__)


@dataclass
class RetrievedPassage:
    """A retrieved knowledge passage with relevance score.

    Attributes:
        text: The passage content.
        score: Similarity score (0-1, higher = more similar).
        source: Source document identifier.
        metadata: Additional metadata.
    """

    text: str
    score: float
    source: str = ""
    metadata: dict = field(default_factory=dict)


class Retriever:
    """Retrieves relevant passages from the vector store.

    Filters results by similarity threshold and formats them
    for inclusion in the system prompt.
    """

    def __init__(
        self,
        vector_store: VectorStore,
        top_k: int = 5,
        similarity_threshold: float = 0.3,
    ) -> None:
        """Initialize the retriever.

        Args:
            vector_store: The VectorStore instance to query.
            top_k: Maximum number of passages to return.
            similarity_threshold: Minimum similarity score (0-1) to include.
        """
        self._vector_store = vector_store
        self._top_k = top_k
        self._similarity_threshold = similarity_threshold
        logger.debug("Retriever initialized: top_k=%d, threshold=%.2f",
                      top_k, similarity_threshold)

    def retrieve(self, query: str) -> list[RetrievedPassage]:
        """Retrieve relevant passages for a query.

        Args:
            query: The search query.

        Returns:
            List of RetrievedPassage objects sorted by relevance.
        """
        if not query or not query.strip():
            return []

        results = self._vector_store.query(query_text=query, n_results=self._top_k)

        passages: list[RetrievedPassage] = []
        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        for doc, meta, dist in zip(documents, metadatas, distances):
            similarity = 1 - dist
            if similarity >= self._similarity_threshold:
                passages.append(RetrievedPassage(
                    text=doc,
                    score=similarity,
                    source=meta.get("source", "unknown"),
                    metadata=meta,
                ))

        passages.sort(key=lambda p: p.score, reverse=True)
        logger.info("Retrieved %d passages (threshold=%.2f) for query: %s...",
                     len(passages), self._similarity_threshold, query[:50])
        return passages

    def format_for_prompt(self, passages: list[RetrievedPassage]) -> str:
        """Format retrieved passages as context for the system prompt.

        Args:
            passages: List of RetrievedPassage objects.

        Returns:
            Formatted string of passages.
        """
        if not passages:
            return ""

        lines = []
        for i, p in enumerate(passages, 1):
            lines.append(f"[{i}] (similarity: {p.score:.2f}) {p.text}")
        return "\n\n".join(lines)
