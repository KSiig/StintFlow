"""Public accessor for the sessions collection."""

from pymongo.collection import Collection

from .helpers._get_collection import _get_collection


def get_sessions_collection() -> Collection:
    """Get the sessions collection."""
    return _get_collection("sessions")
