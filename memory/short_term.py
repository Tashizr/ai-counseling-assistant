"""
Short-term memory for the current conversation session.

Maintains a sliding window of recent messages and context
for the conversation engine.
"""

import logging
from collections import deque
from dataclasses import dataclass, field
from typing import Optional

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """A single conversation message.

    Attributes:
        role: 'user' or 'assistant'.
        content: Message content.
        emotion: Detected emotion (if user message).
        risk_level: Risk level (if user message).
    """

    role: str
    content: str
    emotion: Optional[str] = None
    risk_level: Optional[str] = None


class ShortTermMemory:
    """Manages short-term memory for the current conversation.

    Maintains a fixed-size sliding window of recent messages,
    the user's current mood, and active conversation goals.
    """

    def __init__(self, max_messages: int = 50) -> None:
        """Initialize short-term memory.

        Args:
            max_messages: Maximum number of messages to retain.
        """
        self._max_messages = max_messages
        self._messages: deque[Message] = deque(maxlen=max_messages)
        self._user_name: Optional[str] = None
        self._current_mood: Optional[str] = None
        self._mood_score: Optional[int] = None
        self._current_goals: list[str] = []
        self._mentioned_strategies: list[str] = []
        self._recent_topics: list[str] = []
        logger.debug("ShortTermMemory initialized: max_messages=%d", max_messages)

    def add_message(self, message: Message) -> None:
        """Add a message to short-term memory.

        Args:
            message: The Message to add.
        """
        self._messages.append(message)
        logger.debug("Added message: role=%s, length=%d", message.role, len(message.content))

    def get_recent_messages(self, count: Optional[int] = None) -> list[Message]:
        """Return the most recent messages.

        Args:
            count: Number of messages to return. None returns all.

        Returns:
            List of recent Message objects.
        """
        if count is None:
            return list(self._messages)
        return list(self._messages)[-count:]

    def get_context_string(self) -> str:
        """Format recent messages as context for the system prompt.

        Returns:
            Formatted string of recent conversation turns.
        """
        if not self._messages:
            return ""

        lines = []
        for msg in self._messages:
            prefix = "User" if msg.role == "user" else "Assistant"
            lines.append(f"{prefix}: {msg.content[:200]}")
        return "\n".join(lines)

    def set_user_name(self, name: str) -> None:
        """Set the user's name.

        Args:
            name: The user's name.
        """
        self._user_name = name
        logger.debug("User name set: %s", name)

    def update_mood(self, mood: str, score: Optional[int] = None) -> None:
        """Update the current mood state.

        Args:
            mood: Emotion label for current mood.
            score: Optional numeric mood score (1-10).
        """
        self._current_mood = mood
        self._mood_score = score
        logger.debug("Mood updated: %s (score=%s)", mood, score)

    def add_goal(self, goal: str) -> None:
        """Add a goal to the current conversation.

        Args:
            goal: A conversation goal.
        """
        if goal not in self._current_goals:
            self._current_goals.append(goal)

    def add_strategy(self, strategy: str) -> None:
        """Record a mentioned coping strategy.

        Args:
            strategy: A coping strategy mentioned by the user.
        """
        if strategy not in self._mentioned_strategies:
            self._mentioned_strategies.append(strategy)

    def add_topic(self, topic: str) -> None:
        """Add a topic to recent topics.

        Args:
            topic: A discussion topic.
        """
        if topic not in self._recent_topics:
            self._recent_topics.append(topic)
            if len(self._recent_topics) > 10:
                self._recent_topics.pop(0)

    @property
    def user_name(self) -> Optional[str]:
        """Return the user's name."""
        return self._user_name

    @property
    def current_mood(self) -> Optional[str]:
        """Return the current mood."""
        return self._current_mood

    @property
    def mood_score(self) -> Optional[int]:
        """Return the current mood score."""
        return self._mood_score

    @property
    def message_count(self) -> int:
        """Return the number of stored messages."""
        return len(self._messages)

    def clear(self) -> None:
        """Clear all short-term memory."""
        self._messages.clear()
        self._user_name = None
        self._current_mood = None
        self._mood_score = None
        self._current_goals.clear()
        self._mentioned_strategies.clear()
        self._recent_topics.clear()
        logger.info("Short-term memory cleared")
