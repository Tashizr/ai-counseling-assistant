"""Tests for the database module."""

import pytest
from database.connection import DatabaseManager
from database.models import initialize_database, get_current_version


class TestDatabaseManager:
    """Tests for database connection and operations."""

    def test_connection(self, db_manager):
        conn = db_manager.get_connection()
        assert conn is not None

    def test_execute_and_fetch(self, db_manager):
        db_manager.execute(
            "INSERT INTO conversations (id, user_id) VALUES (?, ?)",
            ("test-conv-1", "test-user"),
        )
        result = db_manager.fetch_one(
            "SELECT * FROM conversations WHERE id = ?", ("test-conv-1",)
        )
        assert result is not None
        assert result["user_id"] == "test-user"

    def test_fetch_all(self, db_manager):
        for i in range(3):
            db_manager.execute(
                "INSERT INTO conversations (id, user_id) VALUES (?, ?)",
                (f"conv-{i}", "test-user"),
            )
        results = db_manager.fetch_all(
            "SELECT * FROM conversations WHERE user_id = ?", ("test-user",)
        )
        assert len(results) == 3

    def test_context_manager(self, tmp_path):
        db_path = str(tmp_path / "ctx_test.db")
        with DatabaseManager(db_path) as db:
            db.execute("SELECT 1")
        # Connection should be closed after exiting context

    def test_schema_version(self, db_manager):
        version = get_current_version(db_manager)
        assert version == 1


class TestDatabaseModels:
    """Tests for database schema initialization."""

    def test_initialize_creates_tables(self, db_manager):
        tables = db_manager.fetch_all(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        table_names = [t["name"] for t in tables]
        assert "conversations" in table_names
        assert "messages" in table_names
        assert "user_profiles" in table_names
        assert "mood_entries" in table_names
        assert "memory_entries" in table_names

    def test_initialize_idempotent(self, db_manager):
        initialize_database(db_manager)
        initialize_database(db_manager)
        tables = db_manager.fetch_all(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
        assert len(tables) >= 6
