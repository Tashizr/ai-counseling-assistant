"""
ChromaDB vector store interface for the RAG pipeline.

Manages collection creation, document storage, and similarity search.
"""

import logging
from typing import Optional

import chromadb
from chromadb.config import Settings as ChromaSettings
from chromadb.api.types import EmbeddingFunction, Documents, Embeddings

logger = logging.getLogger(__name__)


class SentenceTransformerEmbedding(EmbeddingFunction):
    """Custom embedding function using Sentence Transformers."""

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self._model_name = model_name
        self._model = None

    def _ensure_model(self):
        if self._model is None:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self._model_name)

    def __call__(self, input: Documents) -> Embeddings:
        self._ensure_model()
        embeddings = self._model.encode(input, show_progress_bar=False)
        return embeddings.tolist()


class VectorStore:
    """ChromaDB-based vector store for document embeddings.

    Provides document ingestion, collection management, and
    similarity-based retrieval.
    """

    def __init__(
        self,
        persist_dir: str = "./chroma_db",
        collection_name: str = "counseling_knowledge",
        embedding_model: str = "all-MiniLM-L6-v2",
    ) -> None:
        """Initialize the vector store.

        Args:
            persist_dir: Directory for ChromaDB persistence.
            collection_name: Name of the collection to use.
            embedding_model: Sentence transformer model name for embeddings.
        """
        self._persist_dir = persist_dir
        self._collection_name = collection_name
        self._embedding_fn = SentenceTransformerEmbedding(embedding_model)
        self._client = chromadb.PersistentClient(
            path=persist_dir,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
            embedding_function=self._embedding_fn,
        )
        logger.info("VectorStore initialized: collection=%s, dir=%s, model=%s",
                     collection_name, persist_dir, embedding_model)

    def add_documents(
        self,
        texts: list[str],
        metadatas: Optional[list[dict]] = None,
        ids: Optional[list[str]] = None,
    ) -> None:
        """Add documents to the vector store.

        Args:
            texts: List of text chunks to store.
            metadatas: Optional list of metadata dicts.
            ids: Optional list of document IDs. Auto-generated if not provided.
        """
        if not texts:
            return

        if ids is None:
            existing_count = self._collection.count()
            ids = [f"doc_{existing_count + i}" for i in range(len(texts))]

        if metadatas is None:
            metadatas = [{} for _ in texts]

        self._collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
        )
        logger.info("Added %d documents to collection '%s'",
                     len(texts), self._collection_name)

    def query(
        self,
        query_text: str,
        n_results: int = 5,
        where: Optional[dict] = None,
    ) -> dict:
        """Query the vector store for similar documents.

        Args:
            query_text: The query text.
            n_results: Number of results to return.
            where: Optional metadata filter.

        Returns:
            Dictionary with 'documents', 'metadatas', 'distances', 'ids'.
        """
        results = self._collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where,
        )
        logger.debug("Query returned %d results for: %s...",
                      len(results.get("documents", [[]])[0]), query_text[:50])
        return results

    def delete_all(self) -> None:
        """Delete all documents from the collection."""
        self._client.delete_collection(self._collection_name)
        self._collection = self._client.get_or_create_collection(
            name=self._collection_name,
            metadata={"hnsw:space": "cosine"},
            embedding_function=self._embedding_fn,
        )
        logger.info("Deleted all documents from collection '%s'", self._collection_name)

    @property
    def count(self) -> int:
        """Return the number of documents in the collection."""
        return self._collection.count()
