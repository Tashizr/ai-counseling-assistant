"""
Text processing utility functions.
"""

import re
from typing import Optional


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """Truncate text to a maximum length with suffix.

    Args:
        text: Input text.
        max_length: Maximum character length.
        suffix: Suffix to append when truncated.

    Returns:
        Truncated text.
    """
    if len(text) <= max_length:
        return text
    return text[: max_length - len(suffix)] + suffix


def extract_name_from_message(text: str) -> Optional[str]:
    """Try to extract a user's name from their message.

    Looks for common patterns like "I'm [name]", "my name is [name]",
    "call me [name]", etc.

    Args:
        text: The user's message.

    Returns:
        Extracted name, or None if not found.
    """
    patterns = [
        r"(?:i'm|i am|my name is|call me|i'm called)\s+([A-Z][a-z]+)",
        r"(?:i'm|i am|my name is|call me|i'm called)\s+([A-Z][a-z]+ [A-Z][a-z]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1).strip()
            if len(name) >= 2 and len(name) <= 30:
                return name

    return None


def format_duration(seconds: int) -> str:
    """Format a duration in seconds to a human-readable string.

    Args:
        seconds: Duration in seconds.

    Returns:
        Formatted duration string.
    """
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"
