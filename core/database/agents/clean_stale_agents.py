"""
Remove agent records that have not sent a heartbeat recently.

This is intended to be invoked periodically by any running tracker process
so that the ``agents`` collection doesn't accumulate stale entries when
tracker instances crash or are abandoned.  The operation is designed to be
simple and atomic; a single ``delete_many`` query is used so that multiple
trackers can perform the cleanup concurrently without interfering with one
another.

The grace period defaults to one minute (60 seconds) as requested by the
UI logic, and callers typically poll at a much higher frequency (every
5 seconds is sufficient since the stale threshold is large).

Return value mirrors other database helpers: ``True`` on success (even if
no documents were removed), ``False`` on error.  Errors are logged using the
same structured logging conventions as the rest of the database layer.
"""
from datetime import datetime, timezone, timedelta
from pymongo.errors import PyMongoError

from ..connection import get_agents_collection
from core.errors import log


def clean_stale_agents(grace_period_seconds: int = 60) -> bool:
    """Delete agents whose ``last_heartbeat`` is older than the cutoff.

    Args:
        grace_period_seconds: Number of seconds an agent may go without a
            heartbeat before being considered stale.  Must be positive.

    Returns:
        True if the operation succeeded (even if zero documents were
        deleted); False if a database error occurred.
    """
    if not isinstance(grace_period_seconds, (int, float)) or grace_period_seconds <= 0:
        raise ValueError("grace_period_seconds must be a positive number")

    cutoff = datetime.now(timezone.utc) - timedelta(seconds=grace_period_seconds)
    try:
        agents_col = get_agents_collection()
        result = agents_col.delete_many({"last_heartbeat": {"$lt": cutoff}})
        if result.deleted_count:
            log('INFO', f'Removed {result.deleted_count} stale agent(s)',
                category='database', action='clean_stale_agents')
        else:
            log('DEBUG', 'No stale agents to remove',
                category='database', action='clean_stale_agents')
        return True
    except PyMongoError as e:
        log('ERROR', f'Database error cleaning stale agents: {e}',
            category='database', action='clean_stale_agents')
        return False
    except Exception as e:
        log('ERROR', f'Failed to clean stale agents: {e}',
            category='database', action='clean_stale_agents')
        return False
