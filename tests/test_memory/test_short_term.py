"""Tests for ShortTermMemory."""

import pytest
from memory.short_term import ShortTermMemory, Message


class TestShortTermMemory:
    """Tests for short-term memory functionality."""

    def setup_method(self):
        self.memory = ShortTermMemory(max_messages=10)

    def test_add_message(self):
        msg = Message(role="user", content="Hello")
        self.memory.add_message(msg)
        assert self.memory.message_count == 1

    def test_max_messages(self):
        for i in range(15):
            self.memory.add_message(Message(role="user", content=f"Message {i}"))
        assert self.memory.message_count == 10

    def test_get_recent_messages(self):
        for i in range(5):
            self.memory.add_message(Message(role="user", content=f"Message {i}"))
        recent = self.memory.get_recent_messages(3)
        assert len(recent) == 3
        assert recent[0].content == "Message 2"

    def test_context_string(self):
        self.memory.add_message(Message(role="user", content="Hello"))
        self.memory.add_message(Message(role="assistant", content="Hi there"))
        ctx = self.memory.get_context_string()
        assert "User: Hello" in ctx
        assert "Assistant: Hi there" in ctx

    def test_user_name(self):
        assert self.memory.user_name is None
        self.memory.set_user_name("Alex")
        assert self.memory.user_name == "Alex"

    def test_mood_update(self):
        self.memory.update_mood("anxious", score=4)
        assert self.memory.current_mood == "anxious"
        assert self.memory.mood_score == 4

    def test_clear(self):
        self.memory.add_message(Message(role="user", content="Test"))
        self.memory.set_user_name("Test")
        self.memory.clear()
        assert self.memory.message_count == 0
        assert self.memory.user_name is None
