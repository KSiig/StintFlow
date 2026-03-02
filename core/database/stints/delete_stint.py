"""
Delete a stint document from the database.

This helper is the counterpart to :func:`update_stint`.  It removes the
specified document by its ObjectId.  The function is intentionally simple
because the application stores little state about a deleted document; once
it is gone there is nothing left to retrieve.

The UI uses this when the user explicitly requests that a recorded stint be
removed.  Calling code is responsible for ensuring the corresponding row is
removed from any in‑memory data structures after the database operation
succeeds.
"""

from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

from ..connection import get_stints_collection
from core.errors import log


def delete_stint(stint_id: str) -> bool:
    """
    Remove a stint from the database.

    Args:
        stint_id: String representation of the document _id.

    Returns:
        ``True`` if the document was successfully deleted, ``False`` if the
        document could not be found or an error occurred.

    Raises:
        ValueError: if ``stint_id`` is missing.
    """
    if not stint_id:
        raise ValueError("stint_id is required")

    try:
        obj_id = ObjectId(str(stint_id))
        stints_col = get_stints_collection()
        result = stints_col.delete_one({"_id": obj_id})

        if result.deleted_count > 0:
            log('DEBUG', f'Deleted stint {stint_id}',
                category='database', action='delete_stint')
            return True

        log('WARNING', f'Stint {stint_id} not found for deletion',
            category='database', action='delete_stint')
        return False

    except PyMongoError as e:
        log('ERROR', f'Database error deleting stint {stint_id}: {e}',
            category='database', action='delete_stint')
        return False
    except Exception as e:
        log('ERROR', f'Failed to delete stint {stint_id}: {e}',
            category='database', action='delete_stint')
        return False
