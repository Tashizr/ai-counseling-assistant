"""Tests for the Retriever."""

import pytest
from rag.vector_store import VectorStore
from rag.retriever import Retriever, RetrievedPassage


class TestRetriever:
    """Tests for RAG retrieval functionality."""

    def test_retrieve_empty_store(self, tmp_path):
        vs = VectorStore(
            persist_dir=str(tmp_path / "test_chroma"),
            collection_name="test",
        )
        retriever = Retriever(vs)
        results = retriever.retrieve("anxiety management")
        assert len(results) == 0

    def test_retrieve_with_documents(self, tmp_path):
        vs = VectorStore(
            persist_dir=str(tmp_path / "test_chroma2"),
            collection_name="test2",
        )
        vs.add_documents(
            texts=[
                "CBT helps identify negative thought patterns",
                "Deep breathing can reduce anxiety",
                "Exercise improves mental health",
            ],
            metadatas=[
                {"source": "cbt_guide"},
                {"source": "anxiety_tips"},
                {"source": "exercise_benefits"},
            ],
        )

        retriever = Retriever(vs, top_k=2)
        results = retriever.retrieve("how to manage anxiety")
        assert len(results) <= 2
        assert all(isinstance(r, RetrievedPassage) for r in results)

    def test_format_for_prompt(self):
        passages = [
            RetrievedPassage(text="CBT is effective", score=0.8, source="test"),
            RetrievedPassage(text="Mindfulness helps", score=0.6, source="test2"),
        ]
        retriever = Retriever.__new__(Retriever)
        formatted = retriever.format_for_prompt(passages)
        assert "CBT is effective" in formatted
        assert "Mindfulness helps" in formatted

    def test_format_empty_passages(self):
        retriever = Retriever.__new__(Retriever)
        formatted = retriever.format_for_prompt([])
        assert formatted == ""
