"""
Data models for the memory system.
"""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class MemoryEntry:
    """A single memory entry.

    Attributes:
        id: Unique identifier.
        user_id: Associated user ID.
        category: 'short_term' or 'long_term'.
        content: The memory content text.
        importance: Importance score (1-5).
        created_at: Creation timestamp.
        accessed_at: Last access timestamp.
        expires_at: Optional expiration timestamp.
    """

    id: str = ""
    user_id: str = ""
    category: str = "short_term"
    content: str = ""
    importance: int = 3
    created_at: str = ""
    accessed_at: str = ""
    expires_at: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for storage."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "category": self.category,
            "content": self.content,
            "importance": self.importance,
            "created_at": self.created_at,
            "accessed_at": self.accessed_at,
            "expires_at": self.expires_at,
        }


@dataclass
class ConversationSummary:
    """A summary of a conversation session.

    Attributes:
        conversation_id: The conversation identifier.
        summary: Summary text.
        topics: List of main topics discussed.
        mood_start: Starting mood score.
        mood_end: Ending mood score.
        risk_level_max: Highest risk level during conversation.
    """

    conversation_id: str = ""
    summary: str = ""
    topics: list[str] = field(default_factory=list)
    mood_start: Optional[int] = None
    mood_end: Optional[int] = None
    risk_level_max: str = "low"
