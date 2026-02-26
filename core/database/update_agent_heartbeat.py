"""
Update the heartbeat timestamp for a named agent.

This is intended to be called periodically by a running tracker so that the
UI can determine which agents are still alive.  If the agent name is not
found we log a warning; callers should normally register the agent first
using :func:`register_agent`.
"""

from datetime import datetime, timezone
from pymongo.errors import PyMongoError

from .connection import get_agents_collection
from core.errors import log


def update_agent_heartbeat(name: str) -> bool:
    """Refresh the ``last_heartbeat`` field for the given agent.

    Args:
        name: Name of the agent to update.

    Returns:
        True on success (even if no matching document existed), False on
        database error.
    """
    if not name or not isinstance(name, str):
        raise ValueError("agent name must be a non-empty string")

    try:
        agents_col = get_agents_collection()
        now = datetime.now(timezone.utc)
        result = agents_col.update_one(
            {"name": name},
            {"$set": {"last_heartbeat": now}},
        )
        if result.matched_count == 0:
            log('WARNING', f'Heartbeat update for unknown agent "{name}"',
                category='database', action='update_agent_heartbeat')
        else:
            log('DEBUG', f'Heartbeat updated for agent "{name}"',
                category='database', action='update_agent_heartbeat')
        return True
    except PyMongoError as e:
        log('ERROR', f'Database error updating heartbeat for agent {name}: {e}',
            category='database', action='update_agent_heartbeat')
        return False
    except Exception as e:
        log('ERROR', f'Failed to update heartbeat for agent {name}: {e}',
            category='database', action='update_agent_heartbeat')
        return False
