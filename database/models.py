"""
Database schema definitions and initialization.

Defines all tables, indexes, and provides functions to initialize
the database and run schema migrations.
"""

import logging
from typing import Optional

from database.connection import DatabaseManager

logger = logging.getLogger(__name__)

SCHEMA_VERSION = 1

TABLES = {
    "conversations": """
        CREATE TABLE IF NOT EXISTS conversations (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            started_at TEXT NOT NULL DEFAULT (datetime('now')),
            ended_at TEXT,
            summary TEXT,
            mood_start INTEGER,
            mood_end INTEGER,
            risk_level_max TEXT DEFAULT 'low',
            created_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """,
    "messages": """
        CREATE TABLE IF NOT EXISTS messages (
            id TEXT PRIMARY KEY,
            conversation_id TEXT NOT NULL,
            role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
            content TEXT NOT NULL,
            emotion_primary TEXT,
            emotion_confidence REAL,
            risk_level TEXT DEFAULT 'low',
            timestamp TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
        )
    """,
    "user_profiles": """
        CREATE TABLE IF NOT EXISTS user_profiles (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            preferences TEXT DEFAULT '{}',
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            updated_at TEXT NOT NULL DEFAULT (datetime('now'))
        )
    """,
    "mood_entries": """
        CREATE TABLE IF NOT EXISTS mood_entries (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            conversation_id TEXT,
            mood_score INTEGER NOT NULL CHECK (mood_score BETWEEN 1 AND 10),
            emotions TEXT DEFAULT '[]',
            notes TEXT,
            timestamp TEXT NOT NULL DEFAULT (datetime('now')),
            FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE SET NULL
        )
    """,
    "memory_entries": """
        CREATE TABLE IF NOT EXISTS memory_entries (
            id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            category TEXT NOT NULL CHECK (category IN ('short_term', 'long_term')),
            content TEXT NOT NULL,
            importance INTEGER NOT NULL CHECK (importance BETWEEN 1 AND 5),
            created_at TEXT NOT NULL DEFAULT (datetime('now')),
            accessed_at TEXT NOT NULL DEFAULT (datetime('now')),
            expires_at TEXT
        )
    """,
}

INDEXES = [
    "CREATE INDEX IF NOT EXISTS idx_messages_conversation ON messages(conversation_id)",
    "CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp)",
    "CREATE INDEX IF NOT EXISTS idx_conversations_user ON conversations(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_conversations_started ON conversations(started_at)",
    "CREATE INDEX IF NOT EXISTS idx_mood_entries_user ON mood_entries(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_mood_entries_conversation ON mood_entries(conversation_id)",
    "CREATE INDEX IF NOT EXISTS idx_memory_entries_user ON memory_entries(user_id)",
    "CREATE INDEX IF NOT EXISTS idx_memory_entries_category ON memory_entries(category)",
]

SCHEMA_VERSION_TABLE = """
    CREATE TABLE IF NOT EXISTS schema_version (
        version INTEGER PRIMARY KEY,
        applied_at TEXT NOT NULL DEFAULT (datetime('now')),
        description TEXT
    )
"""


def initialize_database(db: DatabaseManager) -> None:
    """Create all tables and indexes if they don't exist.

    Args:
        db: The DatabaseManager instance to initialize.
    """
    logger.info("Initializing database schema")

    db.execute(SCHEMA_VERSION_TABLE)

    for table_name, create_sql in TABLES.items():
        db.execute(create_sql)
        logger.debug("Created/verified table: %s", table_name)

    for index_sql in INDEXES:
        db.execute(index_sql)

    current_version = get_current_version(db)
    if current_version < SCHEMA_VERSION:
        db.execute(
            "INSERT OR IGNORE INTO schema_version (version, description) VALUES (?, ?)",
            (SCHEMA_VERSION, "Initial schema"),
        )
        logger.info("Schema version set to %d", SCHEMA_VERSION)

    logger.info("Database initialization complete")


def get_current_version(db: DatabaseManager) -> int:
    """Return the current schema version.

    Args:
        db: The DatabaseManager instance.

    Returns:
        The current schema version number, or 0 if no version exists.
    """
    row = db.fetch_one("SELECT MAX(version) as version FROM schema_version")
    if row and row["version"] is not None:
        return int(row["version"])
    return 0


def run_migrations(db: DatabaseManager) -> None:
    """Run any pending schema migrations.

    Args:
        db: The DatabaseManager instance to migrate.
    """
    current = get_current_version(db)
    logger.info("Current schema version: %d", current)
    if current >= SCHEMA_VERSION:
        logger.info("Schema is up to date")
    else:
        logger.warning(
            "Schema version %d is newer than current %d — manual migration may be needed",
            SCHEMA_VERSION,
            current,
        )
