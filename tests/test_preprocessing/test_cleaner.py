"""Tests for the TextCleaner."""

import pytest
from preprocessing.cleaner import TextCleaner


class TestTextCleaner:
    """Tests for text cleaning functionality."""

    def setup_method(self):
        self.cleaner = TextCleaner()

    def test_clean_whitespace(self):
        result = self.cleaner.clean("  Hello   world  ")
        assert result == "Hello world"

    def test_clean_urls(self):
        result = self.cleaner.clean("Visit https://example.com for info")
        assert "https://" not in result

    def test_clean_empty(self):
        result = self.cleaner.clean("")
        assert result is None

    def test_clean_too_short(self):
        result = self.cleaner.clean("hi")
        assert result is None

    def test_clean_preserves_content(self):
        result = self.cleaner.clean("CBT is a therapy approach for anxiety")
        assert "CBT" in result
        assert "anxiety" in result

    def test_clean_batch(self):
        texts = ["Hello world", "Too short", "Another valid text"]
        results = self.cleaner.clean_batch(texts)
        assert len(results) == 2

    def test_lowercase(self):
        cleaner = TextCleaner(lowercase=True)
        result = cleaner.clean("Hello WORLD")
        assert result == "hello world"
