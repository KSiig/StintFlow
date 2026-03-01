"""Defaults for logging settings."""

import os


def _get_default_logging_settings(self) -> dict:
    """Return default logging settings from environment or defaults."""
    return {"retention_days": int(os.getenv("LOG_RETENTION_DAYS", "7"))}
