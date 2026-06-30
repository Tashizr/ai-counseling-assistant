"""
Input validation utility functions.
"""

from typing import Optional


def validate_mood_score(score: int) -> bool:
    """Validate a mood score is within acceptable range.

    Args:
        score: The mood score to validate.

    Returns:
        True if valid (1-10), False otherwise.
    """
    return 1 <= score <= 10


def validate_risk_level(level: str) -> bool:
    """Validate a risk level string.

    Args:
        level: The risk level to validate.

    Returns:
        True if valid, False otherwise.
    """
    return level in ("low", "moderate", "high", "critical")


def validate_user_id(user_id: str) -> bool:
    """Validate a user ID.

    Args:
        user_id: The user ID to validate.

    Returns:
        True if valid, False otherwise.
    """
    return bool(user_id and len(user_id) <= 100)


def sanitize_input(text: str, max_length: int = 5000) -> Optional[str]:
    """Sanitize user input text.

    Args:
        text: Raw user input.
        max_length: Maximum allowed length.

    Returns:
        Sanitized text, or None if invalid.
    """
    if not text or not isinstance(text, str):
        return None

    cleaned = text.strip()
    if len(cleaned) > max_length:
        cleaned = cleaned[:max_length]

    if not cleaned:
        return None

    return cleaned
