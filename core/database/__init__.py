"""
Barrel file for database operations.

Exports database operation functions and collection references.
"""

from .get_events import get_events
from .get_sessions import get_sessions
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
    'stints_col',
    'events_col',
    'sessions_col',
    'teams_col',
    'strategies_col',
    'close_connection',
]
