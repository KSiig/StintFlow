"""Persist the session's tyre inventory at green flag.

This helper will overwrite the value on each call; callers should enforce
"only once" semantics if needed (e.g. the processor uses a local flag).
"""

from bson.objectid import ObjectId
from pymongo.errors import PyMongoError

from core.errors import log, log_exception

from ..connection import get_sessions_collection


def set_tires_remaining_at_green_flag(session_id: str, tires_remaining: int) -> bool:
    """Set ``tires_remaining_at_green_flag`` on the session document.

    The field is overwritten each call.  Use caller-side logic to ensure
    the value is written only once if required.
    """
    if not session_id:
        raise ValueError("session_id is required")

    if isinstance(tires_remaining, bool) or not isinstance(tires_remaining, int):
        raise ValueError("tires_remaining must be an integer")

    if tires_remaining < 0:
        raise ValueError("tires_remaining must be a non-negative integer")

    try:
        session_obj_id = ObjectId(session_id)
        sessions_col = get_sessions_collection()
        # always set/overwrite the field; the caller is responsible for
        # determining whether it should be invoked multiple times.
        result = sessions_col.update_one(
            {"_id": session_obj_id},
            {"$set": {"tires_remaining_at_green_flag": tires_remaining}},
        )

        if result.matched_count > 0:
            log(
                'INFO',
                f'Set tires remaining at green flag to: {tires_remaining}',
                category='database',
                action='set_tires_remaining_at_green_flag',
            )
            return True

        log(
            'WARNING',
            f'Session {session_id} not found, could not set green-flag tire count',
            category='database',
            action='set_tires_remaining_at_green_flag',
        )
        return False

    except PyMongoError as e:
        log_exception(
            e,
            f'Database error saving green-flag tire snapshot for session {session_id}',
            category='database',
            action='set_tires_remaining_at_green_flag',
        )
        return False
    except Exception as e:
        log_exception(
            e,
            f'Failed to save green-flag tire snapshot for session {session_id}',
            category='database',
            action='set_tires_remaining_at_green_flag',
        )
        return False