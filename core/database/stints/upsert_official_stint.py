"""
Upsert official stint document.

Ensures only one official stint exists for a given stint key.
"""

from typing import Any
from pymongo.errors import PyMongoError
from core.errors import log, log_exception
from ..connection import get_stints_collection


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

        # If we inserted a new document, return the new id
        if result.upserted_id:
            return str(result.upserted_id), True

        # Document already exists. If the incoming tire compound values in the
        # provided `stint` are *real* (not "Unknown"), update those fields on
        # the existing document so tracker instances with better telemetry can
        # enrich earlier records.
        updates: dict[str, object] = {}
        tire_data = stint.get('tire_data', {}) or {}
        for pos, pos_data in tire_data.items():
            try:
                incoming = pos_data.get('incoming', {})
                compound = incoming.get('compound')
            except Exception:
                compound = None

            if isinstance(compound, str) and compound.strip().lower() != 'unknown':
                updates[f"tire_data.{pos}.incoming.compound"] = compound

        if updates:
            try:
                upd_res = stints_col.update_one(filter_doc, {"$set": updates})
                if upd_res.modified_count > 0:
                    log('DEBUG', f'Enriched existing stint {stint_key} with compounds: {list(updates.keys())}',
                        category='database', action='upsert_official_stint')
            except PyMongoError as e:
                log_exception(e, 'Failed to enrich existing stint with incoming compounds',
                              category='database', action='upsert_official_stint')

        # Return existing id (defensive fetch)
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
