"""
Data models for risk detection results.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class RiskResult:
    """Result of risk level classification.

    Attributes:
        level: Risk level classification (low, moderate, high, critical).
        confidence: Confidence score (0-1) for the classification.
        signals: List of detected risk signals.
        requires_crisis_resources: Whether to show crisis resources.
        requires_professional_referral: Whether to suggest professional help.
    """

    level: str = "low"
    confidence: float = 0.0
    signals: list[str] = field(default_factory=list)
    requires_crisis_resources: bool = False
    requires_professional_referral: bool = False

    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "level": self.level,
            "confidence": self.confidence,
            "signals": self.signals,
            "requires_crisis_resources": self.requires_crisis_resources,
            "requires_professional_referral": self.requires_professional_referral,
        }
