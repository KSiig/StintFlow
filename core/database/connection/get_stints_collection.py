"""Public accessor for the stints collection."""

from pymongo.collection import Collection

from .helpers._get_collection import _get_collection


def get_stints_collection() -> Collection:
    """Get the stints collection."""
    return _get_collection("stints")
