"""
Risk signal extraction from conversation text.

Identifies specific indicators that contribute to risk classification.
"""

import re
import logging
from typing import Optional

from emotion_detection.keywords import CRISIS_KEYWORDS, HIGH_RISK_KEYWORDS

logger = logging.getLogger(__name__)


class SignalExtractor:
    """Extracts risk signals from text for classification.

    Uses pattern matching and linguistic cues to identify specific
    risk indicators in user messages.
    """

    def __init__(self) -> None:
        """Initialize the signal extractor with compiled patterns."""
        self._crisis_patterns = [
            re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE)
            for kw in CRISIS_KEYWORDS
        ]
        self._high_risk_patterns = [
            re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE)
            for kw in HIGH_RISK_KEYWORDS
        ]
        self._isolation_patterns = [
            re.compile(r"\b(alone|nobody|no one|isolated|abandoned|no friends)\b", re.IGNORECASE),
            re.compile(r"\b(everyone left|no one cares|forgotten|invisible)\b", re.IGNORECASE),
        ]
        self._hopelessness_patterns = [
            re.compile(r"\b(hopeless|no hope|no point|give up|nothing will change)\b", re.IGNORECASE),
            re.compile(r"\b(never get better|trapped|no way out|stuck forever)\b", re.IGNORECASE),
        ]
        self._intensity_patterns = [
            re.compile(r"!{2,}"),
            re.compile(r"[A-Z]{4,}"),
        ]

    def extract(self, text: str) -> dict[str, bool]:
        """Extract risk signals from text.

        Args:
            text: The user's message text.

        Returns:
            Dict of signal names to whether they were detected.
        """
        signals = {
            "crisis_language": False,
            "high_risk_language": False,
            "isolation": False,
            "hopelessness": False,
            "emotional_intensity": False,
        }

        for pattern in self._crisis_patterns:
            if pattern.search(text):
                signals["crisis_language"] = True
                break

        for pattern in self._high_risk_patterns:
            if pattern.search(text):
                signals["high_risk_language"] = True
                break

        for pattern in self._isolation_patterns:
            if pattern.search(text):
                signals["isolation"] = True
                break

        for pattern in self._hopelessness_patterns:
            if pattern.search(text):
                signals["hopelessness"] = True
                break

        for pattern in self._intensity_patterns:
            if pattern.search(text):
                signals["emotional_intensity"] = True
                break

        detected = [k for k, v in signals.items() if v]
        if detected:
            logger.info("Risk signals detected: %s", detected)

        return signals

    def extract_detailed(self, text: str) -> dict[str, list[str]]:
        """Extract detailed risk signals with matched patterns.

        Args:
            text: The user's message text.

        Returns:
            Dict of signal names to lists of matched phrases.
        """
        details: dict[str, list[str]] = {
            "crisis_language": [],
            "high_risk_language": [],
            "isolation": [],
            "hopelessness": [],
            "emotional_intensity": [],
        }

        for kw in CRISIS_KEYWORDS:
            if re.search(rf"\b{re.escape(kw)}\b", text, re.IGNORECASE):
                details["crisis_language"].append(kw)

        for kw in HIGH_RISK_KEYWORDS:
            if re.search(rf"\b{re.escape(kw)}\b", text, re.IGNORECASE):
                details["high_risk_language"].append(kw)

        for pattern in self._isolation_patterns:
            matches = pattern.findall(text)
            details["isolation"].extend(matches)

        for pattern in self._hopelessness_patterns:
            matches = pattern.findall(text)
            details["hopelessness"].extend(matches)

        for pattern in self._intensity_patterns:
            matches = pattern.findall(text)
            details["emotional_intensity"].extend(matches)

        return details
