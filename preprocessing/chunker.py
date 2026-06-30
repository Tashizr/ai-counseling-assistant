"""
Semantic text chunking for RAG pipeline.

Splits documents into meaningful chunks that preserve context
for embedding and retrieval.
"""

import logging
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class Chunk:
    """A text chunk with metadata.

    Attributes:
        text: The chunk content.
        chunk_id: Unique identifier for the chunk.
        source: Source document identifier.
        start_char: Starting character index in original text.
        end_char: Ending character index in original text.
        metadata: Additional metadata dictionary.
    """

    text: str
    chunk_id: str = ""
    source: str = ""
    start_char: int = 0
    end_char: int = 0
    metadata: dict = field(default_factory=dict)


class SemanticChunker:
    """Splits text into semantic chunks with overlap for context preservation.

    Uses paragraph and sentence boundaries to create meaningful chunks
    that maintain context for embedding and retrieval.
    """

    _SENTENCE_ENDINGS = r"(?<=[.!?])\s+"

    def __init__(
        self,
        max_chunk_size: int = 512,
        min_chunk_size: int = 50,
        overlap: int = 50,
    ) -> None:
        """Initialize the semantic chunker.

        Args:
            max_chunk_size: Maximum characters per chunk.
            min_chunk_size: Minimum characters per chunk.
            overlap: Number of characters to overlap between chunks.
        """
        self._max_chunk_size = max_chunk_size
        self._min_chunk_size = min_chunk_size
        self._overlap = overlap
        logger.debug("SemanticChunker: max=%d, min=%d, overlap=%d",
                      max_chunk_size, min_chunk_size, overlap)

    def chunk(
        self,
        text: str,
        source: str = "",
        metadata: Optional[dict] = None,
    ) -> list[Chunk]:
        """Split text into semantic chunks.

        Args:
            text: Input text to chunk.
            source: Source document identifier.
            metadata: Optional metadata to attach to each chunk.

        Returns:
            List of Chunk objects.
        """
        if not text or not text.strip():
            return []

        paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

        chunks: list[Chunk] = []
        chunk_index = 0
        current_text = ""
        current_start = 0

        for paragraph in paragraphs:
            if len(current_text) + len(paragraph) + 1 <= self._max_chunk_size:
                current_text = f"{current_text}\n\n{paragraph}" if current_text else paragraph
            else:
                if current_text and len(current_text) >= self._min_chunk_size:
                    chunks.append(Chunk(
                        text=current_text.strip(),
                        chunk_id=f"{source}_chunk_{chunk_index}",
                        source=source,
                        start_char=current_start,
                        end_char=current_start + len(current_text),
                        metadata=metadata or {},
                    ))
                    chunk_index += 1

                if len(paragraph) > self._max_chunk_size:
                    sub_chunks = self._split_large_paragraph(paragraph, source, chunk_index, metadata)
                    chunks.extend(sub_chunks)
                    chunk_index += len(sub_chunks)
                    current_text = ""
                    current_start = 0
                else:
                    current_start = current_start + len(current_text) - self._overlap
                    current_text = paragraph

        if current_text and len(current_text) >= self._min_chunk_size:
            chunks.append(Chunk(
                text=current_text.strip(),
                chunk_id=f"{source}_chunk_{chunk_index}",
                source=source,
                start_char=current_start,
                end_char=current_start + len(current_text),
                metadata=metadata or {},
            ))

        logger.info("Chunked '%s': %d chunks from %d chars", source, len(chunks), len(text))
        return chunks

    def _split_large_paragraph(
        self,
        text: str,
        source: str,
        start_index: int,
        metadata: Optional[dict],
    ) -> list[Chunk]:
        """Split a paragraph that exceeds max_chunk_size into sentence-based chunks.

        Args:
            text: The oversized paragraph.
            source: Source identifier.
            start_index: Starting chunk index.
            metadata: Metadata to attach.

        Returns:
            List of Chunk objects.
        """
        import re
        sentences = re.split(self._SENTENCE_ENDINGS, text)
        chunks: list[Chunk] = []
        current_text = ""
        chunk_index = start_index

        for sentence in sentences:
            if len(current_text) + len(sentence) + 1 <= self._max_chunk_size:
                current_text = f"{current_text} {sentence}" if current_text else sentence
            else:
                if current_text and len(current_text) >= self._min_chunk_size:
                    chunks.append(Chunk(
                        text=current_text.strip(),
                        chunk_id=f"{source}_chunk_{chunk_index}",
                        source=source,
                        start_char=0,
                        end_char=len(current_text),
                        metadata=metadata or {},
                    ))
                    chunk_index += 1
                current_text = sentence

        if current_text and len(current_text) >= self._min_chunk_size:
            chunks.append(Chunk(
                text=current_text.strip(),
                chunk_id=f"{source}_chunk_{chunk_index}",
                source=source,
                start_char=0,
                end_char=len(current_text),
                metadata=metadata or {},
            ))

        return chunks

    def chunk_batch(
        self,
        documents: list[dict],
    ) -> list[Chunk]:
        """Chunk multiple documents.

        Args:
            documents: List of dicts with 'text', 'source', and optional 'metadata'.

        Returns:
            Combined list of all chunks.
        """
        all_chunks: list[Chunk] = []
        for doc in documents:
            chunks = self.chunk(
                text=doc.get("text", ""),
                source=doc.get("source", ""),
                metadata=doc.get("metadata"),
            )
            all_chunks.extend(chunks)
        logger.info("Batch chunking complete: %d chunks from %d documents",
                     len(all_chunks), len(documents))
        return all_chunks
