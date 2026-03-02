"""
Remove an agent document from the database.

This can be used when an agent shuts down cleanly and wishes to unregister
itself.  Most of the time the UI will rely on heartbeat timestamps and may
ignore deleted entries, but having a delete operation simplifies tests and
manual cleanup.
"""

from pymongo.errors import PyMongoError

from ..connection import get_agents_collection
from core.errors import log
import socket

def delete_agent(name: str) -> bool:
    """Delete the agent record with the given name.

    Args:
        name: Name of the agent to remove.

    Returns:
        True if a document was deleted or the operation succeeded; False on
        database error.
    """
    if not name:
        name = socket.gethostname()
    elif not isinstance(name, str):
        raise ValueError("agent name must be a string")

    try:
        agents_col = get_agents_collection()
        result = agents_col.delete_one({"name": name})
        if result.deleted_count:
            log('DEBUG', f'Deleted agent "{name}"',
                category='database', action='delete_agent')
        else:
            log('DEBUG', f'No agent document found to delete: "{name}"',
                category='database', action='delete_agent')
        return True
    except PyMongoError as e:
        log('ERROR', f'Database error deleting agent {name}: {e}',
            category='database', action='delete_agent')
        return False
    except Exception as e:
        log('ERROR', f'Failed to delete agent {name}: {e}',
            category='database', action='delete_agent')
        return False
