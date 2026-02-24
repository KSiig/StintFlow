"""
Register or update an agent (tracker) in the database.

An "agent" represents an independent process that is connected to the
application (for example, a stint tracker instance).  We store a document
for each agent so that the UI can show all currently connected processes
and their last heartbeat time.

Registration is idempotent.  If an agent document with the given name
already exists we simply update its ``last_heartbeat`` field; otherwise a
new document is inserted and ``connected_at`` is also set.

The implementation uses ``update_one`` with ``upsert=True`` to handle
both cases in one database round-trip.
"""

from datetime import datetime, timezone
from pymongo.errors import PyMongoError

from .connection import get_agents_collection
from core.errors import log


def register_agent(name: str) -> bool:
    """Insert or refresh an agent record.

    Args:
        name: Unique name for the agent instance (e.g. "stint_tracker_1234").

    Returns:
        True on success, False on error.
    """
    if not name or not isinstance(name, str):
        raise ValueError("agent name must be a non-empty string")

    try:
        agents_col = get_agents_collection()
        now = datetime.now(timezone.utc)
        agents_col.update_one(
            {"name": name},
            {
                "$setOnInsert": {"connected_at": now},
                "$set": {"last_heartbeat": now},
            },
            upsert=True,
        )
        log('DEBUG', f'Registered/updated agent "{name}"',
            category='database', action='register_agent')
        return True
    except PyMongoError as e:
        log('ERROR', f'Database error registering agent {name}: {e}',
            category='database', action='register_agent')
        return False
    except Exception as e:
        log('ERROR', f'Failed to register agent {name}: {e}',
            category='database', action='register_agent')
        return False
