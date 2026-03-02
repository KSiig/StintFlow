"""Resolve a baseline pit-end time used in practice-mode tracking.

When running in practice mode the tracker computes remaining time
relative to the most recent pit end. This helper prefers the latest
stint document (sorted by pit_end_time_bucket) and falls back to the
configured event `length` when no stints exist yet.
"""

from typing import Any

from core.database import (
    get_session,
    get_event,
    get_latest_stint,
)
from core.errors import log, log_exception


def _get_practice_baseline_time(session_id: str) -> str | None:
    """
    Get baseline time for practice mode tracking.

    Practice tracking always calculates remaining time relative to the
    *previous* pit end.  When a tracker is restarted mid‑session we need
    to know what the most recent pit record is so that the offset can be
    applied correctly.  The earlier implementation simply called
    :func:`get_stints` and took ``stints[-1]``.  Mongo cursors are not
    guaranteed to return documents in chronological order, which meant the
    "latest" stint could be wrong and the calculated lap time would be
    completely off.

    The new version asks the database for the latest stint explicitly
    (sorted by ``pit_end_time_bucket``) and falls back to the event length
    only if no stints exist at all.

    Args:
        session_id: Database session ID

    Returns:
        Baseline time in HH:MM:SS format, or ``None`` if the session or
        race cannot be loaded (which should normally not happen).
    """
    # Prefer the most-recently recorded official stint
    try:
        latest = get_latest_stint(session_id)
    except Exception as e:
        log_exception(e, "Failed to fetch latest stint",
                      category="stint_tracker", action="get_practice_baseline_time")
        latest = None

    if latest:
        return latest.get("pit_end_time")

    # No stints yet: fall back to the session's event length
    try:
        session = get_session(session_id)
    except Exception as e:
        log_exception(e, "Failed to load session",
                      category="stint_tracker", action="get_practice_baseline_time")
        return None

    if not session:
        log("WARNING", f"Session not found: {session_id}",
            category="stint_tracker", action="get_practice_baseline_time")
        return None

    try:
        event = get_event(str(session["race_id"]))
    except Exception as e:
        log_exception(e, "Failed to load event for session",
                      category="stint_tracker", action="get_practice_baseline_time")
        return None

    if not event:
        log("WARNING", f"Event not found for session: {session_id}",
            category="stint_tracker", action="get_practice_baseline_time")
        return None

    return event.get("length")