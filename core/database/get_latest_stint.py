"""
Retrieve the most recent stint for a session.

This helper is used by practice mode tracking to determine the baseline
"pit end" time when the tracker restarts mid-session.  The previous
implementation simply called :func:`get_stints` and grabbed the last item
of the returned list, but the Mongo cursor is **not** sorted so the order
was effectively arbitrary.  That could lead to a stale or incorrect
time being used as the baseline which in turn made the remaining-time
calculation wrong.

The new function performs a sorted query on the normalized bucket field
(`pit_end_time_bucket`) which is zero‑padded and therefore sorts
chronologically when compared lexicographically.  We return ``None`` if no
stints are found or an error occurs.
"""

from bson.objectid import ObjectId

from .connection import get_stints_collection
from core.errors import log


def get_latest_stint(session_id: str) -> dict | None:
    """
    Retrieve the most recent stint document for a given session.

    Args:
        session_id: String representation of the session ObjectId

    Returns:
        The newest stint document by ``pit_end_time_bucket`` or ``None`` if
        there are no stints or an error is encountered.

    Raises:
        ValueError: If ``session_id`` is falsy or invalid.
    """
    if not session_id:
        raise ValueError("session_id is required")

    try:
        session_obj_id = ObjectId(session_id)
        stints_col = get_stints_collection()
        # sort descending so the first document is the latest
        cursor = stints_col.find(
            {"session_id": session_obj_id, "$or":
             [{"official": True}, {"official": {"$exists": False}}]},
        ).sort("pit_end_time_bucket", -1).limit(1)

        latest = None
        for doc in cursor:
            latest = doc
            break

        if latest:
            log('DEBUG',
                f"Retrieved latest stint {latest.get('_id')} for session {session_id}",
                category='database', action='get_latest_stint')
        else:
            log('DEBUG', f"No stints found for session {session_id}",
                category='database', action='get_latest_stint')

        return latest
    except Exception as e:
        log('ERROR', f'Failed to fetch latest stint for session {session_id}: {e}',
            category='database', action='get_latest_stint')
        return None
