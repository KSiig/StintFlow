"""
Tire management utilities.

Tools for tracking tire wear, compounds, and changes during pit stops.
"""

from .get_tire_state import get_tire_state
from .get_tire_wear import get_tire_wear
from .get_tire_compound import get_tire_compound
from .detect_tire_changes import detect_tire_changes
from .constants import (
    TIRE_POSITIONS, 
    TIRE_INDEX_MAP,
    COMPOUND_MAP,
    WEAR_COMPARISON_EPSILON
)

__all__ = [
    'get_tire_state',
    'get_tire_wear',
    'get_tire_compound',
    'detect_tire_changes',
    'TIRE_POSITIONS',
    'TIRE_INDEX_MAP',
    'COMPOUND_MAP',
    'WEAR_COMPARISON_EPSILON'
]
