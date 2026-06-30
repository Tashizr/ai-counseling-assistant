"""
Long-term memory using SQLite for persistent storage.

Stores conversation summaries, user preferences, progress tracking,
and important memories that persist across sessions.
"""

import json
import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from database.connection import DatabaseManager

logger = logging.getLogger(__name__)


class LongTermMemory:
    """Manages persistent memory stored in SQLite.

    Provides CRUD operations for memory entries, conversation summaries,
    user preferences, and mood tracking data.
    """

    def __init__(self, db: DatabaseManager) -> None:
        """Initialize long-term memory with a database connection.

        Args:
            db: The DatabaseManager instance.
        """
        self._db = db
        logger.debug("LongTermMemory initialized")

    def store_memory(
        self,
        user_id: str,
        content: str,
        category: str = "long_term",
        importance: int = 3,
        expires_at: Optional[str] = None,
    ) -> str:
        """Store a memory entry.

        Args:
            user_id: The user identifier.
            content: Memory content text.
            category: 'short_term' or 'long_term'.
            importance: Importance score (1-5).
            expires_at: Optional expiration timestamp.

        Returns:
            The ID of the created memory entry.
        """
        memory_id = str(uuid.uuid4())
        now = datetime.now(timezone.utc).isoformat()
        self._db.execute(
            """INSERT INTO memory_entries (id, user_id, category, content, importance, created_at, accessed_at, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
            (memory_id, user_id, category, content, importance, now, now, expires_at),
        )
        logger.debug("Stored memory: id=%s, category=%s, importance=%d", memory_id, category, importance)
        return memory_id

    def retrieve_memories(
        self,
        user_id: str,
        category: Optional[str] = None,
        limit: int = 10,
        min_importance: int = 1,
    ) -> list[dict]:
        """Retrieve memory entries for a user.

        Args:
            user_id: The user identifier.
            category: Optional filter by category.
            limit: Maximum entries to return.
            min_importance: Minimum importance score.

        Returns:
            List of memory entry dictionaries.
        """
        query = "SELECT * FROM memory_entries WHERE user_id = ? AND importance >= ?"
        params: list = [user_id, min_importance]

        if category:
            query += " AND category = ?"
            params.append(category)

        query += " ORDER BY importance DESC, created_at DESC LIMIT ?"
        params.append(limit)

        results = self._db.fetch_all(query, tuple(params))

        for row in results:
            self._db.execute(
                "UPDATE memory_entries SET accessed_at = ? WHERE id = ?",
                (datetime.now(timezone.utc).isoformat(), row["id"]),
            )

        logger.debug("Retrieved %d memories for user %s", len(results), user_id)
        return results

    def store_conversation_summary(
        self,
        conversation_id: str,
        summary: str,
        mood_start: Optional[int] = None,
        mood_end: Optional[int] = None,
        risk_level_max: str = "low",
    ) -> None:
        """Store a conversation summary.

        Args:
            conversation_id: The conversation identifier.
            summary: Summary text.
            mood_start: Starting mood score.
            mood_end: Ending mood score.
            risk_level_max: Highest risk level during conversation.
        """
        self._db.execute(
            """UPDATE conversations
            SET summary = ?, mood_start = ?, mood_end = ?, risk_level_max = ?, ended_at = ?
            WHERE id = ?""",
            (summary, mood_start, mood_end, risk_level_max, datetime.now(timezone.utc).isoformat(), conversation_id),
        )
        logger.info("Stored conversation summary: %s", conversation_id)

    def get_conversation_summaries(
        self,
        user_id: str,
        limit: int = 10,
    ) -> list[dict]:
        """Retrieve past conversation summaries.

        Args:
            user_id: The user identifier.
            limit: Maximum summaries to return.

        Returns:
            List of conversation dictionaries with summaries.
        """
        results = self._db.fetch_all(
            """SELECT id, started_at, ended_at, summary, mood_start, mood_end, risk_level_max
            FROM conversations
            WHERE user_id = ? AND summary IS NOT NULL
            ORDER BY started_at DESC LIMIT ?""",
            (user_id, limit),
        )
        return results

    def store_user_preference(self, user_id: str, key: str, value: str) -> None:
        """Store a user preference.

        Args:
            user_id: The user identifier.
            key: Preference key.
            value: Preference value.
        """
        profile = self._db.fetch_one(
            "SELECT preferences FROM user_profiles WHERE id = ?", (user_id,)
        )
        if profile:
            prefs = json.loads(profile["preferences"])
            prefs[key] = value
            self._db.execute(
                "UPDATE user_profiles SET preferences = ?, updated_at = ? WHERE id = ?",
                (json.dumps(prefs), datetime.now(timezone.utc).isoformat(), user_id),
            )
        else:
            self._db.execute(
                "INSERT INTO user_profiles (id, name, preferences) VALUES (?, ?, ?)",
                (user_id, user_id, json.dumps({key: value})),
            )
        logger.debug("Stored preference: user=%s, key=%s", user_id, key)

    def get_user_preference(self, user_id: str, key: str, default: Optional[str] = None) -> Optional[str]:
        """Retrieve a user preference.

        Args:
            user_id: The user identifier.
            key: Preference key.
            default: Default value if preference not found.

        Returns:
            The preference value, or default.
        """
        profile = self._db.fetch_one(
            "SELECT preferences FROM user_profiles WHERE id = ?", (user_id,)
        )
        if profile:
            prefs = json.loads(profile["preferences"])
            return prefs.get(key, default)
        return default

    def get_mood_history(self, user_id: str, limit: int = 30) -> list[dict]:
        """Retrieve mood tracking history.

        Args:
            user_id: The user identifier.
            limit: Maximum entries to return.

        Returns:
            List of mood entry dictionaries.
        """
        return self._db.fetch_all(
            """SELECT mood_score, emotions, timestamp
            FROM mood_entries
            WHERE user_id = ?
            ORDER BY timestamp DESC LIMIT ?""",
            (user_id, limit),
        )

    def store_mood_entry(
        self,
        user_id: str,
        mood_score: int,
        emotions: list[str],
        conversation_id: Optional[str] = None,
        notes: Optional[str] = None,
    ) -> str:
        """Store a mood tracking entry.

        Args:
            user_id: The user identifier.
            mood_score: Mood score (1-10).
            emotions: List of emotion labels.
            conversation_id: Optional conversation identifier.
            notes: Optional notes.

        Returns:
            The ID of the created mood entry.
        """
        entry_id = str(uuid.uuid4())
        self._db.execute(
            """INSERT INTO mood_entries (id, user_id, conversation_id, mood_score, emotions, notes)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (entry_id, user_id, conversation_id, mood_score, json.dumps(emotions), notes),
        )
        logger.debug("Stored mood entry: user=%s, score=%d", user_id, mood_score)
        return entry_id

    def cleanup_expired(self) -> int:
        """Remove expired memory entries.

        Returns:
            Number of entries removed.
        """
        now = datetime.now(timezone.utc).isoformat()
        result = self._db.execute(
            "DELETE FROM memory_entries WHERE expires_at IS NOT NULL AND expires_at < ?",
            (now,),
        )
        count = result.rowcount
        if count > 0:
            logger.info("Cleaned up %d expired memory entries", count)
        return count
