"""Public accessor for the agents collection."""

from pymongo.collection import Collection

from core.errors import log
from .helpers._get_collection import _get_collection


def get_agents_collection() -> Collection:
    """Get the agents collection and ensure the name index exists."""
    col = _get_collection("agents")
    try:
        col.create_index("name", unique=True)
    except Exception:
        log(
            "WARNING",
            "Failed to create unique index on agents.name",
            category="database",
            action="get_agents_collection",
        )
    return col
