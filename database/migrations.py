"""
Database migration system for schema versioning.

Provides a simple migration framework that tracks applied versions
and supports forward migrations.
"""

import logging
from dataclasses import dataclass
from typing import List

from database.connection import DatabaseManager
from database.models import SCHEMA_VERSION

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Migration:
    """A single database migration.

    Attributes:
        version: Schema version this migration targets.
        description: Human-readable description of the migration.
        up_sql: SQL statements to apply the migration.
        down_sql: SQL statements to revert the migration.
    """

    version: int
    description: str
    up_sql: str
    down_sql: str


MIGRATIONS: List[Migration] = [
    Migration(
        version=1,
        description="Initial schema with all tables",
        up_sql="",
        down_sql="",
    ),
]


def get_current_version(db: DatabaseManager) -> int:
    """Return the current schema version from the database.

    Args:
        db: DatabaseManager instance.

    Returns:
        Current version number, or 0 if no migrations have been applied.
    """
    row = db.fetch_one("SELECT MAX(version) as version FROM schema_version")
    if row and row["version"] is not None:
        return int(row["version"])
    return 0


def migrate_to_latest(db: DatabaseManager) -> None:
    """Apply all pending migrations to bring the database to the latest version.

    Args:
        db: DatabaseManager instance to migrate.
    """
    current = get_current_version(db)
    pending = [m for m in MIGRATIONS if m.version > current]

    if not pending:
        logger.info("Database is already at the latest version: %d", current)
        return

    for migration in pending:
        logger.info("Applying migration v%d: %s", migration.version, migration.description)
        try:
            if migration.up_sql:
                db.execute(migration.up_sql)
            db.execute(
                "INSERT INTO schema_version (version, description) VALUES (?, ?)",
                (migration.version, migration.description),
            )
            logger.info("Migration v%d applied successfully", migration.version)
        except Exception as e:
            logger.error("Migration v%d failed: %s", migration.version, e)
            raise

    logger.info("All migrations applied. Current version: %d", SCHEMA_VERSION)
