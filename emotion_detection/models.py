"""
Data models for emotion detection results.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class EmotionResult:
    """Result of emotion detection on a text.

    Attributes:
        primary_emotion: The dominant detected emotion.
        confidence: Confidence score (0-1) for the primary emotion.
        secondary_emotion: Optional second most likely emotion.
        secondary_confidence: Confidence for the secondary emotion.
        scores: Full dictionary of all emotion scores.
    """

    primary_emotion: str = "neutral"
    confidence: float = 0.0
    secondary_emotion: Optional[str] = None
    secondary_confidence: float = 0.0
    scores: dict[str, float] = field(default_factory=dict)

    @property
    def is_confident(self) -> bool:
        """Return True if the primary emotion has high confidence."""
        return self.confidence >= 0.6

    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "primary": self.primary_emotion,
            "confidence": self.confidence,
            "secondary": self.secondary_emotion,
            "secondary_confidence": self.secondary_confidence,
            "scores": self.scores,
        }
