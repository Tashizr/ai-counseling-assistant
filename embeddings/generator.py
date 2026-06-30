"""
Embedding generation using Sentence Transformers.

Provides a singleton interface for generating text embeddings
with built-in caching for frequently encoded texts.
"""

import hashlib
import logging
from typing import Optional

import numpy as np

logger = logging.getLogger(__name__)

_embedding_model = None


def _get_model(model_name: str):
    """Lazy-load the sentence transformer model.

    Args:
        model_name: Name of the sentence transformer model.

    Returns:
        The loaded SentenceTransformer model.
    """
    global _embedding_model
    if _embedding_model is None:
        from sentence_transformers import SentenceTransformer
        logger.info("Loading embedding model: %s", model_name)
        _embedding_model = SentenceTransformer(model_name)
        logger.info("Embedding model loaded successfully")
    return _embedding_model


class EmbeddingGenerator:
    """Generates text embeddings using Sentence Transformers.

    Supports single and batch encoding with an in-memory cache
    for frequently encoded texts.
    """

    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        dimension: int = 384,
        cache_size: int = 1000,
    ) -> None:
        """Initialize the embedding generator.

        Args:
            model_name: Sentence transformer model name.
            dimension: Expected embedding dimension.
            cache_size: Maximum number of cached embeddings.
        """
        self._model_name = model_name
        self._dimension = dimension
        self._cache: dict[str, np.ndarray] = {}
        self._cache_size = cache_size
        self._model = None
        logger.debug("EmbeddingGenerator initialized: model=%s, dim=%d", model_name, dimension)

    def _ensure_model(self):
        """Ensure the embedding model is loaded."""
        if self._model is None:
            self._model = _get_model(self._model_name)

    def _cache_key(self, text: str) -> str:
        """Generate a cache key for a text string.

        Args:
            text: Input text.

        Returns:
            MD5 hash of the text.
        """
        return hashlib.md5(text.encode("utf-8")).hexdigest()

    def encode(self, text: str) -> np.ndarray:
        """Generate an embedding for a single text string.

        Args:
            text: Input text to encode.

        Returns:
            NumPy array of shape (dimension,).

        Raises:
            ValueError: If text is empty.
        """
        if not text or not text.strip():
            raise ValueError("Cannot encode empty text")

        key = self._cache_key(text)
        if key in self._cache:
            logger.debug("Cache hit for text: %s...", text[:50])
            return self._cache[key]

        self._ensure_model()
        embedding = self._model.encode(text, show_progress_bar=False)

        if len(self._cache) >= self._cache_size:
            oldest_key = next(iter(self._cache))
            del self._cache[oldest_key]

        self._cache[key] = embedding
        return embedding

    def encode_batch(self, texts: list[str]) -> list[np.ndarray]:
        """Generate embeddings for a batch of texts.

        Args:
            texts: List of input texts.

        Returns:
            List of NumPy embedding arrays.
        """
        if not texts:
            return []

        self._ensure_model()
        uncached_texts = []
        uncached_indices = []
        results: list[Optional[np.ndarray]] = [None] * len(texts)

        for i, text in enumerate(texts):
            key = self._cache_key(text)
            if key in self._cache:
                results[i] = self._cache[key]
            else:
                uncached_texts.append(text)
                uncached_indices.append(i)

        if uncached_texts:
            new_embeddings = self._model.encode(uncached_texts, show_progress_bar=False)
            for idx, embedding in zip(uncached_indices, new_embeddings):
                results[idx] = embedding
                key = self._cache_key(texts[idx])
                if len(self._cache) >= self._cache_size:
                    oldest_key = next(iter(self._cache))
                    del self._cache[oldest_key]
                self._cache[key] = embedding

        logger.info("Encoded batch: %d texts, %d cache hits",
                     len(texts), len(texts) - len(uncached_texts))
        return [r for r in results if r is not None]

    @property
    def dimension(self) -> int:
        """Return the embedding dimension."""
        return self._dimension

    def clear_cache(self) -> None:
        """Clear the embedding cache."""
        self._cache.clear()
        logger.debug("Embedding cache cleared")
