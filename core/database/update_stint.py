"""
Update fields on a stint document in the database.

This function accepts a partial document (`doc`) and applies a
MongoDB `$set` for the provided keys. It is intentionally generic so
callers can update `tire_data` or any other simple top-level fields
without needing separate helper functions.
"""

from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

from .connection import get_stints_collection
from core.errors import log


def update_stint(stint_id: str, doc: dict) -> bool:
    """
    Partially update a stint document.

    Args:
        stint_id: String representation of stint ObjectId
        doc: Dictionary of fields to `$set` on the stint document

    Returns:
        True if update successful, False otherwise

    Raises:
        ValueError: If `stint_id` is missing or `doc` is not provided
    """
    if not stint_id:
        raise ValueError("stint_id is required")

    if not isinstance(doc, dict) or not doc:
        raise ValueError("doc (dict) with at least one field is required for update")

    try:
        stint_obj_id = ObjectId(str(stint_id))
        query = {"_id": stint_obj_id}
        update_doc = {"$set": doc}

        stints_col = get_stints_collection()
        result = stints_col.update_one(query, update_doc)

        if result.matched_count > 0:
            log('DEBUG', f'Updated stint fields {list(doc.keys())} for {stint_id}',
                category='database', action='update_stint')
            return True

        log('WARNING', f'Stint {stint_id} not found',
            category='database', action='update_stint')
        return False

    except PyMongoError as e:
        log('ERROR', f'Database error updating stint {stint_id}: {e}',
            category='database', action='update_stint')
        return False
    except Exception as e:
        log('ERROR', f'Failed to update stint {stint_id}: {e}',
            category='database', action='update_stint')
        return False