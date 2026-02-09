"""
Upsert official stint document.

Ensures only one official stint exists for a given stint key.
"""

from typing import Any
from pymongo.errors import PyMongoError
from core.errors import log, log_exception
from .connection import get_stints_collection


def upsert_official_stint(stint: dict[str, Any], stint_key: str) -> tuple[str, bool]:
    """
    Insert an official stint if it does not already exist.

    Args:
        stint: Stint document to insert
        stint_key: Unique key for deduplication

    Returns:
        Tuple of (stint_id, was_inserted)
    """
    stints_col = get_stints_collection()
    filter_doc = {
        "stint_key": stint_key,
        "official": True
    }

    try:
        result = stints_col.update_one(
            filter_doc,
            {"$setOnInsert": stint},
            upsert=True
        )

        if result.upserted_id:
            return str(result.upserted_id), True

        existing = stints_col.find_one(filter_doc, {"_id": 1})
        if not existing:
            log('ERROR', f'Upsert succeeded but no document found for key {stint_key}',
                category='database', action='upsert_official_stint')
            return "", False

        return str(existing["_id"]), False

    except PyMongoError as e:
        log_exception(e, 'MongoDB error during upsert_official_stint',
                     category='database', action='upsert_official_stint')
        return "", False
    except Exception as e:
        log_exception(e, 'Unexpected error during upsert_official_stint',
                     category='database', action='upsert_official_stint')
        return "", False
