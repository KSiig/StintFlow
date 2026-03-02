"""
Retrieve the list of registered agents from the database.

Agents are sorted by latest heartbeat timestamp so that recently active
processes appear first.  The UI can call this function to populate the
"connected agents" view mentioned in issue #59.
"""

from pymongo.errors import PyMongoError

from ..connection import get_agents_collection
from core.errors import log


def get_agents() -> list[dict]:
    """Return all agent documents sorted by ``last_heartbeat`` descending.

    Returns:
        List of agent documents, empty list on error.
    """
    try:
        agents_col = get_agents_collection()
        agents = list(agents_col.find().sort('last_heartbeat', -1))
        log('DEBUG', f'Retrieved {len(agents)} agents',
            category='database', action='get_agents')
        return agents
    except PyMongoError as e:
        log('ERROR', f'Database error retrieving agents: {e}',
            category='database', action='get_agents')
        return []
    except Exception as e:
        log('ERROR', f'Failed to retrieve agents: {e}',
            category='database', action='get_agents')
        return []
