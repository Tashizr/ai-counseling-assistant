"""
Emotion detection using keyword-based classification with NLP augmentation.

Provides lightweight, explainable emotion detection without requiring
a large ML model, making it suitable for local-first operation.
"""

import logging
import re
from typing import Optional

from emotion_detection.models import EmotionResult
from emotion_detection.keywords import EMOTION_KEYWORDS

logger = logging.getLogger(__name__)


class EmotionDetector:
    """Detects emotions from text using keyword matching with weighted scoring.

    Uses a dictionary-based approach with pattern matching to identify
    primary and secondary emotions in user messages.
    """

    def __init__(self, min_confidence: float = 0.1) -> None:
        """Initialize the emotion detector.

        Args:
            min_confidence: Minimum confidence threshold to report an emotion.
        """
        self._min_confidence = min_confidence
        self._compiled_patterns: dict[str, list[re.Pattern]] = {}
        self._compile_patterns()
        logger.debug("EmotionDetector initialized with %d emotion categories",
                      len(EMOTION_KEYWORDS))

    def _compile_patterns(self) -> None:
        """Pre-compile regex patterns for all emotion keywords."""
        for emotion, keywords in EMOTION_KEYWORDS.items():
            patterns = []
            for kw in keywords:
                escaped = re.escape(kw)
                pattern = re.compile(rf"\b{escaped}\b", re.IGNORECASE)
                patterns.append(pattern)
            self._compiled_patterns[emotion] = patterns

    def detect(self, text: str) -> EmotionResult:
        """Detect emotions in a text string.

        Args:
            text: Input text to analyze.

        Returns:
            EmotionResult with primary and secondary emotions.
        """
        if not text or not text.strip():
            return EmotionResult(primary_emotion="neutral", confidence=0.0)

        text_lower = text.lower()
        scores: dict[str, float] = {}

        for emotion, patterns in self._compiled_patterns.items():
            matches = 0
            for pattern in patterns:
                if pattern.search(text_lower):
                    matches += 1
            if matches > 0:
                base_score = min(matches * 0.3, 1.0)
                intensity_bonus = self._calculate_intensity(text_lower)
                scores[emotion] = min(base_score * (1 + intensity_bonus), 1.0)

        if not scores:
            return EmotionResult(
                primary_emotion="neutral",
                confidence=0.5,
                scores={"neutral": 0.5},
            )

        sorted_emotions = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        primary = sorted_emotions[0]
        secondary = sorted_emotions[1] if len(sorted_emotions) > 1 else None

        return EmotionResult(
            primary_emotion=primary[0],
            confidence=primary[1],
            secondary_emotion=secondary[0] if secondary else None,
            secondary_confidence=secondary[1] if secondary else 0.0,
            scores=scores,
        )

    def _calculate_intensity(self, text: str) -> float:
        """Calculate emotional intensity based on punctuation and caps.

        Args:
            text: Lowercase input text.

        Returns:
            Intensity multiplier (0.0 to 0.5).
        """
        intensity = 0.0

        if "!" in text:
            intensity += min(text.count("!") * 0.05, 0.15)
        if "?" in text:
            intensity += min(text.count("?") * 0.03, 0.1)

        caps_words = sum(1 for w in text.split() if w.isupper() and len(w) > 1)
        if caps_words > 0:
            intensity += min(caps_words * 0.05, 0.15)

        intensifiers = [
            "very", "extremely", "incredibly", "absolutely", "totally",
            "completely", "utterly", "so", "really", "deeply",
        ]
        for word in intensifiers:
            if word in text:
                intensity += 0.05

        return min(intensity, 0.5)

    def detect_batch(self, texts: list[str]) -> list[EmotionResult]:
        """Detect emotions for multiple texts.

        Args:
            texts: List of input texts.

        Returns:
            List of EmotionResult objects.
        """
        return [self.detect(text) for text in texts]
