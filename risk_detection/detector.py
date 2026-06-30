"""
Risk level classification for conversation safety.

Classifies user messages into risk levels using multiple signal types
with a conservative approach to minimize false negatives.
"""

import logging
from typing import Optional

from risk_detection.models import RiskResult
from risk_detection.signals import SignalExtractor

logger = logging.getLogger(__name__)

LEVEL_ORDER = {"low": 0, "moderate": 1, "high": 2, "critical": 3}


class RiskDetector:
    """Classifies risk levels in user messages.

    Uses a conservative approach: prioritizes catching potential risks
    (minimizing false negatives) while providing clear signal reasons.
    """

    def __init__(self) -> None:
        """Initialize the risk detector with signal extractor."""
        self._signal_extractor = SignalExtractor()
        logger.debug("RiskDetector initialized")

    def detect(self, text: str, emotion_scores: Optional[dict] = None) -> RiskResult:
        """Classify the risk level of a user message.

        Args:
            text: The user's message text.
            emotion_scores: Optional emotion scores from EmotionDetector.

        Returns:
            RiskResult with classified level and detected signals.
        """
        signals = self._signal_extractor.extract(text)
        detected_signals = [k for k, v in signals.items() if v]

        level = "low"
        confidence = 0.5
        requires_crisis = False
        requires_referral = False

        if signals["crisis_language"]:
            level = "critical"
            confidence = 0.95
            requires_crisis = True
            requires_referral = True
        elif signals["high_risk_language"] and (signals["hopelessness"] or signals["isolation"]):
            level = "high"
            confidence = 0.85
            requires_crisis = True
            requires_referral = True
        elif signals["high_risk_language"] or (signals["hopelessness"] and signals["isolation"]):
            level = "high"
            confidence = 0.75
            requires_referral = True
        elif signals["hopelessness"] or signals["isolation"]:
            level = "moderate"
            confidence = 0.65
            requires_referral = True
        elif signals["emotional_intensity"]:
            level = "moderate"
            confidence = 0.55
            requires_referral = False

        if emotion_scores:
            sadness_score = emotion_scores.get("sadness", 0)
            hopelessness_score = emotion_scores.get("hopelessness", 0)
            anxiety_score = emotion_scores.get("anxiety", 0)

            if sadness_score > 0.7 and hopelessness_score > 0.5:
                level = self._escalate_level(level)
                confidence = min(confidence + 0.1, 0.95)
                if level in ("high", "critical"):
                    requires_crisis = True
                requires_referral = True

            if anxiety_score > 0.8:
                if level == "low":
                    level = "moderate"
                    requires_referral = True

        result = RiskResult(
            level=level,
            confidence=confidence,
            signals=detected_signals,
            requires_crisis_resources=requires_crisis,
            requires_professional_referral=requires_referral,
        )

        if level != "low":
            logger.warning(
                "Risk level '%s' detected (confidence=%.2f) — signals: %s",
                level, confidence, detected_signals,
            )

        return result

    def _escalate_level(self, current_level: str) -> str:
        """Escalate a risk level by one step.

        Args:
            current_level: The current risk level.

        Returns:
            The next higher risk level.
        """
        escalation = {
            "low": "moderate",
            "moderate": "high",
            "high": "critical",
            "critical": "critical",
        }
        return escalation.get(current_level, current_level)

    def should_trigger_crisis_response(self, result: RiskResult) -> bool:
        """Determine if a crisis response should be triggered.

        Args:
            result: The RiskResult to evaluate.

        Returns:
            True if crisis resources should be displayed.
        """
        return result.level in ("high", "critical") or result.requires_crisis_resources

    def should_suggest_professional(self, result: RiskResult) -> bool:
        """Determine if professional help should be suggested.

        Args:
            result: The RiskResult to evaluate.

        Returns:
            True if professional help referral is recommended.
        """
        return result.level in ("moderate", "high", "critical") or result.requires_professional_referral
