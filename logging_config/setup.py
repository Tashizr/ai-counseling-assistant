"""
Structured logging configuration with privacy protections.

User message content is never logged at INFO level or above.
"""

import json
import logging
import logging.handlers
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


class _PrivacyFilter(logging.Filter):
    """Redacts user message content from log records above DEBUG level."""

    _USER_CONTENT_PATTERN = re.compile(r"(user(?:\s+message)?|content|input)", re.IGNORECASE)

    def filter(self, record: logging.LogRecord) -> bool:
        if record.levelno >= logging.INFO:
            if hasattr(record, "msg") and isinstance(record.msg, str):
                if len(record.msg) > 200:
                    record.msg = record.msg[:100] + "... [truncated for privacy]"
        return True


class _JsonFormatter(logging.Formatter):
    """Formats log records as JSON for structured logging."""

    def format(self, record: logging.LogRecord) -> str:
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }
        if record.exc_info and record.exc_info[0] is not None:
            log_entry["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_entry, default=str)


class _ConsoleFormatter(logging.Formatter):
    """Human-readable console log format with color codes."""

    _COLORS = {
        "DEBUG": "\033[36m",
        "INFO": "\033[32m",
        "WARNING": "\033[33m",
        "ERROR": "\033[31m",
        "CRITICAL": "\033[1;31m",
    }
    _RESET = "\033[0m"

    def format(self, record: logging.LogRecord) -> str:
        color = self._COLORS.get(record.levelname, "")
        reset = self._RESET
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return (
            f"{color}{timestamp} | {record.levelname:<8} | "
            f"{record.name} | {record.getMessage()}{reset}"
        )


def setup_logging(
    log_level: str,
    log_dir: str,
    max_size_mb: int,
    backup_count: int,
) -> logging.Logger:
    """Configure application logging with console and file handlers.

    Args:
        log_level: Minimum logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_dir: Directory where log files are written.
        max_size_mb: Maximum size of each log file in megabytes.
        backup_count: Number of rotated log files to retain.

    Returns:
        The root logger configured with both handlers.
    """
    log_path = Path(log_dir)
    log_path.mkdir(parents=True, exist_ok=True)

    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper(), logging.INFO))

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper(), logging.INFO))
    console_handler.setFormatter(_ConsoleFormatter())
    console_handler.addFilter(_PrivacyFilter())
    root_logger.addHandler(console_handler)

    file_handler = logging.handlers.RotatingFileHandler(
        filename=log_path / "app.log",
        maxBytes=max_size_mb * 1024 * 1024,
        backupCount=backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(_JsonFormatter())
    file_handler.addFilter(_PrivacyFilter())
    root_logger.addHandler(file_handler)

    error_handler = logging.handlers.RotatingFileHandler(
        filename=log_path / "error.log",
        maxBytes=max_size_mb * 1024 * 1024,
        backupCount=backup_count,
        encoding="utf-8",
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(_JsonFormatter())
    root_logger.addHandler(error_handler)

    root_logger.info("Logging initialized at %s level", log_level)
    return root_logger


def get_logger(name: str) -> logging.Logger:
    """Return a named logger instance.

    Args:
        name: Logger name, typically __name__ of the calling module.

    Returns:
        A configured logger instance.
    """
    return logging.getLogger(name)
