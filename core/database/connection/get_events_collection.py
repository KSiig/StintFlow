"""Public accessor for the events collection."""

from pymongo.collection import Collection

from .helpers._get_collection import _get_collection


def get_events_collection() -> Collection:
    """Get the events collection."""
    return _get_collection("events")
