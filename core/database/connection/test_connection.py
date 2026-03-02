"""Connectivity probe for MongoDB."""

from core.errors import log
from .helpers._get_client import _get_client


def test_connection() -> bool:
    """Return True if a connection to MongoDB can be established."""
    try:
        log("INFO", "Testing MongoDB connection...", category="database", action="test_connection")
        _get_client()
        return True
    except Exception:
        return False
