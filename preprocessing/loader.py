"""
Document loading for RAG pipeline.

Supports loading from JSON, TXT, and directory-based sources.
"""

import json
import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class DocumentLoader:
    """Loads documents from various file formats for the RAG pipeline."""

    def __init__(self, base_dir: str = "./datasets") -> None:
        """Initialize the document loader.

        Args:
            base_dir: Base directory for dataset files.
        """
        self._base_dir = Path(base_dir)
        logger.debug("DocumentLoader initialized: %s", self._base_dir)

    def load_json(self, file_path: str) -> list[dict]:
        """Load documents from a JSON file.

        The JSON should contain a list of objects, each with at minimum
        a 'text' field and optionally 'source' and 'metadata' fields.

        Args:
            file_path: Path to the JSON file.

        Returns:
            List of document dictionaries.
        """
        path = Path(file_path)
        if not path.exists():
            logger.warning("JSON file not found: %s", file_path)
            return []

        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not isinstance(data, list):
            data = [data]

        docs = []
        for item in data:
            if "text" in item:
                docs.append({
                    "text": item["text"],
                    "source": item.get("source", path.name),
                    "metadata": item.get("metadata", {}),
                })

        logger.info("Loaded %d documents from %s", len(docs), file_path)
        return docs

    def load_text(self, file_path: str, source: Optional[str] = None) -> list[dict]:
        """Load a single text file as a document.

        Args:
            file_path: Path to the text file.
            source: Optional source identifier. Defaults to filename.

        Returns:
            List containing one document dictionary.
        """
        path = Path(file_path)
        if not path.exists():
            logger.warning("Text file not found: %s", file_path)
            return []

        text = path.read_text(encoding="utf-8")
        return [{
            "text": text,
            "source": source or path.name,
            "metadata": {"file_path": str(path)},
        }]

    def load_directory(self, directory: str, extensions: tuple = (".txt", ".json")) -> list[dict]:
        """Load all matching files from a directory.

        Args:
            directory: Directory path to scan.
            extensions: Tuple of file extensions to include.

        Returns:
            List of document dictionaries.
        """
        dir_path = Path(directory)
        if not dir_path.exists():
            logger.warning("Directory not found: %s", directory)
            return []

        all_docs: list[dict] = []
        for ext in extensions:
            for file_path in dir_path.rglob(f"*{ext}"):
                if ext == ".json":
                    all_docs.extend(self.load_json(str(file_path)))
                elif ext == ".txt":
                    all_docs.extend(self.load_text(str(file_path)))

        logger.info("Loaded %d documents from directory %s", len(all_docs), directory)
        return all_docs

    def load_all(self) -> list[dict]:
        """Load all documents from the base datasets directory.

        Scans datasets/raw/ for supported files.

        Returns:
            Combined list of all loaded documents.
        """
        raw_dir = self._base_dir / "raw"
        if not raw_dir.exists():
            logger.warning("Raw datasets directory not found: %s", raw_dir)
            return []

        docs = self.load_directory(str(raw_dir))
        logger.info("Total documents loaded: %d", len(docs))
        return docs
