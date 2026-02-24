"""
Barrel file for database operations.

Exports database operation functions and collection references.
"""

from .get_events import get_events
from .get_sessions import get_sessions
from .get_session import get_session
from .get_stints import get_stints
from .get_strategies import get_strategies
from .get_event import get_event
from .get_team import get_team
from .update_event import update_event
from .delete_strategy import delete_strategy
from .update_session import update_session
from .update_strategy import update_strategy
from .get_latest_stint import get_latest_stint
from .update_stint import update_stint
from .update_team_drivers import update_team_drivers
from .create_event import create_event
from .create_session import create_session
from .create_strategy import create_strategy
from .upsert_official_stint import upsert_official_stint
from .delete_stint import delete_stint
from .delete_strategy import delete_strategy
# agent registry operations
from .register_agent import register_agent
from .update_agent_heartbeat import update_agent_heartbeat
from .get_agents import get_agents
from .delete_agent import delete_agent

from .connection import (
    close_connection,
    get_stints_collection,
    get_events_collection,
    get_sessions_collection,
    get_teams_collection,
    get_strategies_collection,
    get_agents_collection,
)

__all__ = [
    'get_events',
    'get_sessions',
    'get_session',
    'get_stints',
    'get_strategies',
    'get_event',
    'get_team',
    'update_event',
    'update_session',
    'update_strategy',
    'update_stint',
    'update_team_drivers',
    'create_event',
    'create_session',
    'create_strategy',
    'upsert_official_stint',
    'delete_stint',
    'delete_strategy',
    'get_stints_collection',
    'get_events_collection',
    'get_sessions_collection',
    'get_teams_collection',
    'get_strategies_collection',
    'get_agents_collection',
    'register_agent',
    'update_agent_heartbeat',
    'get_agents',
    'delete_agent',
    'close_connection',
]
