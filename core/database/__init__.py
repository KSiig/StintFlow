"""
Barrel file for database operations.

Exports database operation functions and collection references.
"""

from .get_events import get_events
from .get_sessions import get_sessions
from .get_stints import get_stints
from .get_event import get_event
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
    'get_stints',
    'get_event',
    'stints_col',
    'events_col',
    'sessions_col',
    'teams_col',
    'strategies_col',
    'close_connection',
]
