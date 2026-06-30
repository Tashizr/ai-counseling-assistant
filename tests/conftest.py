"""
Shared pytest fixtures for the test suite.
"""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


@pytest.fixture
def db_manager(tmp_path):
    """Provide a temporary DatabaseManager for testing."""
    from database.connection import DatabaseManager
    from database.models import initialize_database

    db_path = str(tmp_path / "test.db")
    db = DatabaseManager(db_path)
    initialize_database(db)
    yield db
    db.close()


@pytest.fixture
def sample_messages():
    """Provide sample conversation messages for testing."""
    return [
        {"role": "user", "content": "I've been feeling really anxious lately."},
        {"role": "assistant", "content": "I hear that you're feeling anxious. Can you tell me more about what's been causing this?"},
        {"role": "user", "content": "Work has been overwhelming. My boss keeps piling on deadlines."},
        {"role": "assistant", "content": "That sounds like a lot of pressure. How long has this been going on?"},
    ]
