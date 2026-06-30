"""
Session manager — handles conversation lifecycle and persistence.

Creates conversations, tracks state, and persists data to the database.
"""

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from database.connection import DatabaseManager

logger = logging.getLogger(__name__)


class SessionManager:
    """Manages conversation sessions and their lifecycle.

    Handles conversation creation, message storage, and session
    state management using the database.
    """

    def __init__(self, db: DatabaseManager) -> None:
        """Initialize the session manager.

        Args:
            db: The DatabaseManager instance.
        """
        self._db = db
        self._current_conversation_id: Optional[str] = None
        self._user_id: Optional[str] = None
        logger.debug("SessionManager initialized")

    def start_conversation(self, user_id: str) -> str:
        """Start a new conversation session.

        Args:
            user_id: The user identifier.

        Returns:
            The new conversation ID.
        """
        conversation_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        self._db.execute(
            """INSERT INTO conversations (id, user_id, started_at, created_at)
            VALUES (?, ?, ?, ?)""",
            (conversation_id, user_id, now, now),
        )

        self._current_conversation_id = conversation_id
        self._user_id = user_id
        logger.info("Started conversation %s for user %s", conversation_id, user_id)
        return conversation_id

    def end_conversation(self) -> None:
        """End the current conversation session."""
        if self._current_conversation_id:
            self._db.execute(
                "UPDATE conversations SET ended_at = ? WHERE id = ?",
                (datetime.now(timezone.utc).isoformat(), self._current_conversation_id),
            )
            logger.info("Ended conversation %s", self._current_conversation_id)
            self._current_conversation_id = None

    def store_message(
        self,
        role: str,
        content: str,
        emotion_primary: Optional[str] = None,
        emotion_confidence: Optional[float] = None,
        risk_level: str = "low",
    ) -> str:
        """Store a conversation message.

        Args:
            role: 'user' or 'assistant'.
            content: Message content.
            emotion_primary: Detected emotion (for user messages).
            emotion_confidence: Emotion confidence score.
            risk_level: Risk level classification.

        Returns:
            The message ID.
        """
        if not self._current_conversation_id:
            logger.error("No active conversation to store message")
            return ""

        message_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()

        self._db.execute(
            """INSERT INTO messages (id, conversation_id, role, content, emotion_primary, emotion_confidence, risk_level, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                message_id,
                self._current_conversation_id,
                role,
                content,
                emotion_primary,
                emotion_confidence,
                risk_level,
                now,
            ),
        )
        logger.debug("Stored message: id=%s, role=%s", message_id, role)
        return message_id

    def get_conversation_messages(self, conversation_id: Optional[str] = None) -> list[dict]:
        """Retrieve messages for a conversation.

        Args:
            conversation_id: Conversation ID. Uses current if not provided.

        Returns:
            List of message dictionaries.
        """
        conv_id = conversation_id or self._current_conversation_id
        if not conv_id:
            return []

        return self._db.fetch_all(
            """SELECT id, role, content, emotion_primary, emotion_confidence, risk_level, timestamp
            FROM messages
            WHERE conversation_id = ?
            ORDER BY timestamp""",
            (conv_id,),
        )

    def get_recent_conversations(
        self,
        user_id: str,
        limit: int = 10,
    ) -> list[dict]:
        """Retrieve recent conversations for a user.

        Args:
            user_id: The user identifier.
            limit: Maximum conversations to return.

        Returns:
            List of conversation dictionaries.
        """
        return self._db.fetch_all(
            """SELECT id, started_at, ended_at, summary, mood_start, mood_end, risk_level_max
            FROM conversations
            WHERE user_id = ?
            ORDER BY started_at DESC
            LIMIT ?""",
            (user_id, limit),
        )

    @property
    def current_conversation_id(self) -> Optional[str]:
        """Return the current conversation ID."""
        return self._current_conversation_id

    @property
    def is_active(self) -> bool:
        """Return True if a conversation is active."""
        return self._current_conversation_id is not None
