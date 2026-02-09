"""
Pit state detection from LMU data.

Determines when player is pitting, entering/leaving pits, or in garage.
"""

from enum import Enum
from typing import Any
from core.errors import log


# Garage stall indicator value from LMU
IN_GARAGE_VALUE = 1


class PitState(Enum):
    """Pit state values from LMU shared memory."""
    ON_TRACK = 0      # Also when driver joined server but not started
    COMING_IN = 2
    PITTING = 4
    LEAVING = 5


def get_pit_state(player_scoring: Any) -> PitState:
    """
    Get current pit state from player scoring data.
    
    Args:
        player_scoring: LMU player vehicle scoring object
        
    Returns:
        Current PitState enum value, defaults to ON_TRACK if invalid
    """
    try:
        return PitState(player_scoring.mPitState)
    except (ValueError, AttributeError) as e:
        log('WARNING', f'Invalid pit state value: {str(e)}',
            category='stint_tracker', action='get_pit_state')
        return PitState.ON_TRACK


def is_in_garage(player_scoring: Any) -> bool:
    """
    Check if player is currently in the garage.
    
    Args:
        player_scoring: LMU player vehicle scoring object
        
    Returns:
        True if player is in garage, False otherwise
    """
    try:
        return player_scoring.mInGarageStall == IN_GARAGE_VALUE
    except AttributeError as e:
        log('WARNING', f'Failed to check garage status: {str(e)}',
            category='stint_tracker', action='is_in_garage')
        return False
