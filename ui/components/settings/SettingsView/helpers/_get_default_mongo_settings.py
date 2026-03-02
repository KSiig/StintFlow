"""Defaults for MongoDB settings."""

import os


def _get_default_mongo_settings(self) -> dict:
    """Return default MongoDB settings from environment or defaults."""
    return {
        "uri": os.getenv("MONGODB_URI", ""),
        "host": os.getenv("MONGODB_HOST", "localhost:27017"),
        "database": os.getenv("MONGODB_DATABASE", "stintflow"),
        "username": os.getenv("MONGODB_USERNAME", ""),
        "password": os.getenv("MONGODB_PASSWORD", ""),
        "auth_source": os.getenv("MONGODB_AUTH_SOURCE", "admin"),
    }
