"""Public accessor for the teams collection."""

from pymongo.collection import Collection

from .helpers._get_collection import _get_collection


def get_teams_collection() -> Collection:
    """Get the teams collection."""
    return _get_collection("teams")
