"""Tests for LongTermMemory."""

import pytest


class TestLongTermMemory:
    """Tests for long-term memory functionality."""

    def test_store_and_retrieve_memory(self, db_manager):
        from memory.long_term import LongTermMemory

        ltm = LongTermMemory(db_manager)
        memory_id = ltm.store_memory(
            user_id="test_user",
            content="User prefers CBT techniques",
            category="long_term",
            importance=4,
        )
        assert memory_id

        memories = ltm.retrieve_memories("test_user")
        assert len(memories) == 1
        assert memories[0]["content"] == "User prefers CBT techniques"

    def test_user_preferences(self, db_manager):
        from memory.long_term import LongTermMemory

        ltm = LongTermMemory(db_manager)
        ltm.store_user_preference("test_user", "theme", "dark")
        value = ltm.get_user_preference("test_user", "theme")
        assert value == "dark"

    def test_mood_entries(self, db_manager):
        from memory.long_term import LongTermMemory

        ltm = LongTermMemory(db_manager)
        entry_id = ltm.store_mood_entry(
            user_id="test_user",
            mood_score=6,
            emotions=["calm", "hopeful"],
        )
        assert entry_id

        history = ltm.get_mood_history("test_user")
        assert len(history) == 1
        assert history[0]["mood_score"] == 6
