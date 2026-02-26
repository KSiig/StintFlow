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
import socket


def register_agent(name: str) -> bool:
    """Insert a new agent record.

    This function **is not idempotent**.  An agent name must be unique; if a
    document with the given name already exists registration fails and the
    caller can react (for example by generating a different name).

    Heartbeats for already-registered agents should be maintained with
    :func:`update_agent_heartbeat` instead of re-registering.

    Args:
        name: Unique name for the agent instance (e.g. "stint_tracker_1234").

    Returns:
        True on success (new document created).
        False if the name already exists or a database error occurred.
    """
    if not name:
        name = socket.gethostname()
    elif not isinstance(name, str):
        raise ValueError("agent name must be a string")

    try:
        agents_col = get_agents_collection()
        now = datetime.now(timezone.utc)
        try:
            agents_col.insert_one({
                "name": name,
                "connected_at": now,
                "last_heartbeat": now,
            })
            log('DEBUG', f'Registered agent "{name}"',
                category='database', action='register_agent')
            return True, name
        except PyMongoError as e:
            # Duplicate key error is expected if the name already exists.
            if getattr(e, 'code', None) == 11000:
                log('WARNING', f'Agent already exists: "{name}"',
                    category='database', action='register_agent')
                return False, name
            # otherwise fall through to generic handler below
            raise
    except PyMongoError as e:
        log('ERROR', f'Database error registering agent {name}: {e}',
            category='database', action='register_agent')
        return False, name
    except Exception as e:
        log('ERROR', f'Failed to register agent {name}: {e}',
            category='database', action='register_agent')
        return False, name
