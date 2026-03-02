"""
Core stint tracking logic.

Main tracking loop, stint creation, and time calculations.
"""

from .track_session import track_session
from .create_stint import create_stint

__all__ = [
    'track_session',
    'create_stint',
]
