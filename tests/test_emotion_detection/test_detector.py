"""Tests for the EmotionDetector."""

import pytest
from emotion_detection.detector import EmotionDetector
from emotion_detection.models import EmotionResult


class TestEmotionDetector:
    """Tests for emotion detection functionality."""

    def setup_method(self):
        self.detector = EmotionDetector()

    def test_detect_sadness(self):
        result = self.detector.detect("I feel so sad and empty inside")
        assert result.primary_emotion == "sadness"
        assert result.confidence > 0.3

    def test_detect_anxiety(self):
        result = self.detector.detect("I'm really anxious and worried about everything")
        assert result.primary_emotion == "anxiety"
        assert result.confidence > 0.3

    def test_detect_happiness(self):
        result = self.detector.detect("I'm so happy and grateful today!")
        assert result.primary_emotion == "happiness"
        assert result.confidence > 0.3

    def test_detect_anger(self):
        result = self.detector.detect("I'm furious and angry about this situation")
        assert result.primary_emotion == "anger"
        assert result.confidence > 0.3

    def test_detect_loneliness(self):
        result = self.detector.detect("I feel so alone and isolated, nobody cares")
        assert result.primary_emotion == "loneliness"
        assert result.confidence > 0.3

    def test_detect_neutral(self):
        result = self.detector.detect("The weather is okay today")
        assert result.primary_emotion == "neutral"

    def test_empty_input(self):
        result = self.detector.detect("")
        assert result.primary_emotion == "neutral"

    def test_secondary_emotion(self):
        result = self.detector.detect("I'm sad and also very anxious about the future")
        assert result.primary_emotion in ("sadness", "anxiety")
        assert result.secondary_emotion is not None

    def test_intensity_detection(self):
        result1 = self.detector.detect("I'm a little sad")
        result2 = self.detector.detect("I'm EXTREMELY SAD!!!")
        assert result2.confidence >= result1.confidence

    def test_batch_detection(self):
        texts = ["I'm happy", "I'm sad", "I'm angry"]
        results = self.detector.detect_batch(texts)
        assert len(results) == 3
        assert all(isinstance(r, EmotionResult) for r in results)
