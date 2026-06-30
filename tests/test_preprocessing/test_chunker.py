"""Tests for the SemanticChunker."""

import pytest
from preprocessing.chunker import SemanticChunker, Chunk


class TestSemanticChunker:
    """Tests for semantic chunking functionality."""

    def setup_method(self):
        self.chunker = SemanticChunker(max_chunk_size=200, min_chunk_size=20)

    def test_chunk_empty(self):
        chunks = self.chunker.chunk("")
        assert len(chunks) == 0

    def test_chunk_short_text(self):
        text = "This is a short paragraph."
        chunks = self.chunker.chunk(text, source="test")
        assert len(chunks) >= 1
        assert chunks[0].source == "test"

    def test_chunk_long_text(self):
        text = "Paragraph one about anxiety.\n\n" + "Paragraph two about depression. " * 10 + "\n\n" + "Paragraph three about coping."
        chunks = self.chunker.chunk(text)
        assert len(chunks) >= 2

    def test_chunk_metadata(self):
        text = "A valid chunk of text for testing purposes."
        chunks = self.chunker.chunk(text, metadata={"topic": "anxiety"})
        assert chunks[0].metadata == {"topic": "anxiety"}

    def test_chunk_batch(self):
        docs = [
            {"text": "First document content here.", "source": "doc1"},
            {"text": "Second document content here.", "source": "doc2"},
        ]
        chunks = self.chunker.chunk_batch(docs)
        assert len(chunks) >= 2
