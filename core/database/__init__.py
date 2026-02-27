"""
Barrel file for database operations.

Exports database operation functions and collection references.
"""

from .events.get_events import get_events
from .sessions.get_sessions import get_sessions
from .sessions.get_session import get_session
from .stints.get_stints import get_stints
from .strategies.get_strategies import get_strategies
from .events.get_event import get_event
from .teams.get_team import get_team
from .events.update_event import update_event
from .events.delete_strategy import delete_strategy
from .sessions.update_session import update_session
from .strategies.update_strategy import update_strategy
from .stints.get_latest_stint import get_latest_stint
from .stints.update_stint import update_stint
from .teams.update_team_drivers import update_team_drivers
from .events.create_event import create_event
from .sessions.create_session import create_session
from .strategies.create_strategy import create_strategy
from .stints.upsert_official_stint import upsert_official_stint
from .stints.delete_stint import delete_stint
from .events.delete_strategy import delete_strategy
# agent registry operations
from .agents.register_agent import register_agent
from .agents.update_agent_heartbeat import update_agent_heartbeat
from .agents.clean_stale_agents import clean_stale_agents
from .agents.get_agents import get_agents
from .agents.delete_agent import delete_agent

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
