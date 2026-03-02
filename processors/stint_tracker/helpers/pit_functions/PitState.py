"""LMU pit-state constants and small helpers.

This module exposes `PitState` as an ``IntEnum`` so values read directly
from LMU shared memory can be compared to enum members without casting.
The class provides convenience methods for common checks used by the
tracker (e.g. `is_in_pit`).
"""

from enum import IntEnum


class PitState(IntEnum):
    """Pit state values from LMU shared memory.

    Members use the numeric values defined by LMU so integer comparisons
    are natural and efficient.
    """
    ON_TRACK = 0      # Also when driver joined server but not started
    IN_GARAGE = 1
    COMING_IN = 2
    PITTING = 4
    LEAVING = 5