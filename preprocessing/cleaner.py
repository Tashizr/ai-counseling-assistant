"""
Text cleaning and normalization for document preprocessing.

Removes noise, normalizes whitespace, and standardizes formatting
before documents are chunked and embedded.
"""

import re
import logging
from typing import Optional

logger = logging.getLogger(__name__)


class TextCleaner:
    """Cleans and normalizes text content for RAG pipeline ingestion.

    Handles whitespace normalization, special character removal,
    and text normalization while preserving meaningful content.
    """

    _WHITESPACE_PATTERN = re.compile(r"\s+")
    _SPECIAL_CHARS_PATTERN = re.compile(r"[^\w\s.,!?;:'\"()-]")
    _MULTIPLE_PUNCTUATION = re.compile(r"([.,!?;:])\1+")
    _URL_PATTERN = re.compile(r"https?://\S+|www\.\S+")
    _EMAIL_PATTERN = re.compile(r"\S+@\S+\.\S+")

    def __init__(
        self,
        remove_urls: bool = True,
        remove_emails: bool = True,
        lowercase: bool = False,
        min_length: int = 10,
    ) -> None:
        """Initialize the text cleaner.

        Args:
            remove_urls: Whether to strip URLs from text.
            remove_emails: Whether to strip email addresses.
            lowercase: Whether to convert text to lowercase.
            min_length: Minimum character length for valid text.
        """
        self._remove_urls = remove_urls
        self._remove_emails = remove_emails
        self._lowercase = lowercase
        self._min_length = min_length
        logger.debug("TextCleaner initialized: urls=%s, emails=%s, lower=%s",
                      remove_urls, remove_emails, lowercase)

    def clean(self, text: str) -> Optional[str]:
        """Clean and normalize a text string.

        Args:
            text: Raw input text.

        Returns:
            Cleaned text, or None if the result is too short.
        """
        if not text or not text.strip():
            return None

        cleaned = text.strip()

        if self._remove_urls:
            cleaned = self._URL_PATTERN.sub("", cleaned)

        if self._remove_emails:
            cleaned = self._EMAIL_PATTERN.sub("", cleaned)

        cleaned = self._WHITESPACE_PATTERN.sub(" ", cleaned)
        cleaned = self._MULTIPLE_PUNCTUATION.sub(r"\1", cleaned)
        cleaned = self._SPECIAL_CHARS_PATTERN.sub("", cleaned)
        cleaned = self._WHITESPACE_PATTERN.sub(" ", cleaned).strip()

        if self._lowercase:
            cleaned = cleaned.lower()

        if len(cleaned) < self._min_length:
            logger.debug("Text too short after cleaning: %d chars", len(cleaned))
            return None

        return cleaned

    def clean_batch(self, texts: list[str]) -> list[str]:
        """Clean a batch of text strings, filtering out None results.

        Args:
            texts: List of raw input texts.

        Returns:
            List of cleaned texts (None results excluded).
        """
        results = [self.clean(text) for text in texts]
        cleaned = [t for t in results if t is not None]
        logger.info("Cleaned batch: %d -> %d texts", len(texts), len(cleaned))
        return cleaned
