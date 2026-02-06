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
from .update_session import update_session
from .update_strategy import update_strategy
from .update_team_drivers import update_team_drivers
from .create_event import create_event
from .create_session import create_session
from .create_strategy import create_strategy
from .connection import (
    stints_col,
    events_col,
    sessions_col,
    teams_col,
    strategies_col,
    close_connection,
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
    'update_team_drivers',
    'create_event',
    'create_session',
    'create_strategy',
    'stints_col',
    'events_col',
    'sessions_col',
    'teams_col',
    'strategies_col',
    'close_connection',
]
