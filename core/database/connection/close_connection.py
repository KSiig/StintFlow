"""Close the MongoDB connection."""

from core.errors import log, log_exception
from . import _state


def close_connection() -> None:
    """Close the MongoDB connection if it exists."""
    if _state.client is not None:
        try:
            _state.client.close()
            log("INFO", "MongoDB connection closed", category="database", action="close")
        except Exception as exc:
            log_exception(exc, "Error closing MongoDB connection", category="database", action="close")
        finally:
            _state.client = None
            _state.db = None
            _state.db_name = None
