"""Public accessor for the strategies collection."""

from pymongo.collection import Collection

from .helpers._get_collection import _get_collection


def get_strategies_collection() -> Collection:
    """Get the strategies collection."""
    return _get_collection("strategies")
