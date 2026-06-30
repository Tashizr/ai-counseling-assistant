"""
SQLite connection manager with WAL mode and thread-safe access.

Provides a DatabaseManager class that handles connection lifecycle,
query execution, and result formatting.
"""

import sqlite3
import threading
import logging
from pathlib import Path
from typing import Any, Optional

logger = logging.getLogger(__name__)


class DatabaseManager:
    """Manages SQLite database connections with WAL mode and foreign keys.

    Thread-safe via threading.local() connection storage. Supports context
    manager protocol for automatic cleanup.

    Args:
        db_path: File path for the SQLite database. Parent directories
            are created automatically if they don't exist.
    """

    def __init__(self, db_path: str) -> None:
        self._db_path = db_path
        self._local = threading.local()
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        logger.debug("DatabaseManager initialized for %s", db_path)

    def _get_connection(self) -> sqlite3.Connection:
        """Return a thread-local connection, creating one if needed."""
        conn = getattr(self._local, "connection", None)
        if conn is None:
            conn = sqlite3.connect(
                self._db_path,
                timeout=10,
                check_same_thread=False,
            )
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA foreign_keys=ON")
            conn.row_factory = sqlite3.Row
            self._local.connection = conn
            logger.debug("New database connection created for thread %s", threading.current_thread().name)
        return conn

    def get_connection(self) -> sqlite3.Connection:
        """Return a database connection configured with WAL mode and foreign keys.

        Returns:
            A sqlite3.Connection with Row factory and WAL journal mode.
        """
        return self._get_connection()

    def __enter__(self) -> "DatabaseManager":
        """Enter the context manager."""
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Exit the context manager, closing the connection."""
        self.close()

    def execute(self, query: str, params: tuple = ()) -> sqlite3.Cursor:
        """Execute a SQL query and return the cursor.

        Args:
            query: SQL query string with optional parameter placeholders.
            params: Tuple of parameter values for the query.

        Returns:
            The sqlite3.Cursor after execution.

        Raises:
            sqlite3.Error: If the query fails.
        """
        logger.debug("Executing query: %s", query[:100])
        conn = self._get_connection()
        cursor = conn.execute(query, params)
        conn.commit()
        return cursor

    def fetch_one(self, query: str, params: tuple = ()) -> Optional[dict]:
        """Execute a query and return the first result as a dict.

        Args:
            query: SQL query string.
            params: Tuple of parameter values.

        Returns:
            Dictionary of column values, or None if no results.
        """
        logger.debug("Fetching one: %s", query[:100])
        conn = self._get_connection()
        cursor = conn.execute(query, params)
        row = cursor.fetchone()
        if row is None:
            return None
        return dict(row)

    def fetch_all(self, query: str, params: tuple = ()) -> list[dict]:
        """Execute a query and return all results as a list of dicts.

        Args:
            query: SQL query string.
            params: Tuple of parameter values.

        Returns:
            List of dictionaries, one per row.
        """
        logger.debug("Fetching all: %s", query[:100])
        conn = self._get_connection()
        cursor = conn.execute(query, params)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]

    def close(self) -> None:
        """Close the database connection for the current thread."""
        conn = getattr(self._local, "connection", None)
        if conn is not None:
            conn.close()
            self._local.connection = None
            logger.debug("Database connection closed for thread %s", threading.current_thread().name)
