"""
Safety service — multi-layer safety checking for user input and AI output.

Implements input screening, output filtering, and crisis response logic.
"""

import logging
import re
from typing import Optional

from prompts.safety_rules import SAFETY_RULES
from prompts.templates import CRISIS_RESPONSE_TEMPLATE
from risk_detection.detector import RiskDetector
from risk_detection.models import RiskResult
from risk_detection.crisis_resources import get_crisis_resources, format_crisis_resources
from emotion_detection.detector import EmotionDetector
from emotion_detection.models import EmotionResult

logger = logging.getLogger(__name__)

_BLOCKED_PATTERNS = [
    re.compile(r"\b(how to (?:make|build|create) (?:a )?(?:bomb|explosive))\b", re.IGNORECASE),
    re.compile(r"\b(poison|poisoning|overdose instructions?)\b", re.IGNORECASE),
]

_SAFETY_VIOLATION_PATTERNS = [
    re.compile(r"\b(you (?:should|must|need to) (?:kill|harm|hurt))\b", re.IGNORECASE),
    re.compile(r"\b(its? (?:worth|better) (?:nothing|no one))\b", re.IGNORECASE),
    re.compile(r"\b(nobody (?:cares|loves|would miss))\b", re.IGNORECASE),
]


class SafetyService:
    """Multi-layer safety checking for the AI Counseling Assistant.

    Implements:
    1. Input pre-screening (blocked content, crisis detection)
    2. Emotion detection
    3. Risk classification
    4. Output post-checking (policy violations)
    """

    def __init__(self) -> None:
        """Initialize the safety service with component detectors."""
        self._emotion_detector = EmotionDetector()
        self._risk_detector = RiskDetector()
        logger.info("SafetyService initialized")

    def check_input(self, user_message: str) -> dict:
        """Perform full safety check on user input.

        Args:
            user_message: The raw user message.

        Returns:
            Dict with 'emotion', 'risk', 'blocked', 'crisis_triggered', 'requires_response'.
        """
        result = {
            "emotion": None,
            "risk": None,
            "blocked": False,
            "crisis_triggered": False,
            "requires_professional_referral": False,
            "user_message": user_message,
        }

        if self._is_blocked(user_message):
            result["blocked"] = True
            logger.warning("Blocked message detected")
            return result

        emotion = self._emotion_detector.detect(user_message)
        result["emotion"] = emotion

        risk = self._risk_detector.detect(
            user_message,
            emotion_scores=emotion.scores,
        )
        result["risk"] = risk

        if self._risk_detector.should_trigger_crisis_response(risk):
            result["crisis_triggered"] = True
            logger.warning("Crisis response triggered: level=%s", risk.level)

        if self._risk_detector.should_suggest_professional(risk):
            result["requires_professional_referral"] = True

        return result

    def check_output(self, ai_response: str) -> dict:
        """Check AI response for safety violations.

        Args:
            ai_response: The generated AI response.

        Returns:
            Dict with 'is_safe', 'violations', 'sanitized_response'.
        """
        violations = []

        for pattern in _SAFETY_VIOLATION_PATTERNS:
            if pattern.search(ai_response):
                violations.append(f"Pattern matched: {pattern.pattern}")

        has_disclaimer = any(
            keyword in ai_response.lower()
            for keyword in ["ai", "artificial intelligence", "not a therapist", "not a licensed"]
        )

        return {
            "is_safe": len(violations) == 0,
            "violations": violations,
            "has_disclaimer": has_disclaimer,
            "sanitized_response": ai_response,
        }

    def _is_blocked(self, text: str) -> bool:
        """Check if message content should be blocked.

        Args:
            text: User message.

        Returns:
            True if message should be blocked.
        """
        for pattern in _BLOCKED_PATTERNS:
            if pattern.search(text):
                return True
        return False

    def format_crisis_response(self, risk: RiskResult, country_code: str = "DEFAULT") -> str:
        """Format a crisis response with resources.

        Args:
            risk: The RiskResult that triggered crisis response.
            country_code: Country code for resource lookup.

        Returns:
            Formatted crisis response string.
        """
        resources = get_crisis_resources(country_code)
        resource_contact = resources.get("phone", resources.get("text", "See website"))
        return CRISIS_RESPONSE_TEMPLATE.format(
            resource_name=resources["name"],
            resource_contact=resource_contact,
            resource_web=resources.get("web", ""),
        )

    def get_emotion_detector(self) -> EmotionDetector:
        """Return the emotion detector instance."""
        return self._emotion_detector

    def get_risk_detector(self) -> RiskDetector:
        """Return the risk detector instance."""
        return self._risk_detector
