"""
Delete a strategy document from the database.

This helper mirrors :func:`delete_stint` but operates on the
``strategies`` collection.  It is used when the user requests that an
entire strategy be removed; once deleted the UI will remove any associated
tabs or models.
"""

from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

from .connection import get_strategies_collection
from core.errors import log


def delete_strategy(strategy_id: str) -> bool:
    """Remove a strategy from the database.

    Args:
        strategy_id: String representation of the document _id.

    Returns:
        ``True`` if the document was successfully deleted, ``False`` if the
        document could not be found or an error occurred.

    Raises:
        ValueError: if ``strategy_id`` is missing.
    """
    if not strategy_id:
        raise ValueError("strategy_id is required")

    try:
        obj_id = ObjectId(str(strategy_id))
        coll = get_strategies_collection()
        result = coll.delete_one({"_id": obj_id})

        if result.deleted_count > 0:
            log('DEBUG', f'Deleted strategy {strategy_id}',
                category='database', action='delete_strategy')
            return True

        log('WARNING', f'Strategy {strategy_id} not found for deletion',
            category='database', action='delete_strategy')
        return False

    except PyMongoError as e:
        log('ERROR', f'Database error deleting strategy {strategy_id}: {e}',
            category='database', action='delete_strategy')
        return False
    except Exception as e:
        log('ERROR', f'Failed to delete strategy {strategy_id}: {e}',
            category='database', action='delete_strategy')
        return False
