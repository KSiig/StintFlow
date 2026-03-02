"""Helper to fetch a collection from the configured database."""

from pymongo.collection import Collection

from ._get_database import _get_database


def _get_collection(collection_name: str) -> Collection:
    """Return the collection with *collection_name*, ensuring the DB exists."""
    db = _get_database()
    return db[collection_name]
