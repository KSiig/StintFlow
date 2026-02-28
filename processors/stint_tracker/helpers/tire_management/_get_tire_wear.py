"""Calculate tyre wear from a player-vehicle telemetry object.

This module provides a single function, `_get_tire_wear`, which extracts the
wear value for a given tyre position from an LMU `player_vehicle` object.
"""

from typing import Any

from core.errors import log
from .constants import TIRE_INDEX_MAP


def _get_tire_wear(player_vehicle: Any, tire_position: str) -> float:
    """Return the wear value (0.0..1.0) for `tire_position`.

    Args:
        player_vehicle: LMU player vehicle telemetry object expected to have
            an attribute `mWheels` which is an indexable sequence of wheel
            structures exposing `mWear`.
        tire_position: Short position code ("fl","fr","rl","rr").

    Returns:
        Wear value rounded to two decimal places. On any error the function
        logs a warning and returns 0.0.
    """
    try:
        wheel_idx = TIRE_INDEX_MAP[tire_position]
    except KeyError:
        log(
            "WARNING",
            f"Invalid tire position passed to _get_tire_wear: {tire_position}",
            category="stint_tracker",
            action="get_tire_wear",
        )
        return 0.0

    try:
        wheels = getattr(player_vehicle, "mWheels")
        wheel = wheels[wheel_idx]
        wear = float(getattr(wheel, "mWear"))
        return round(wear, 2)
    except (AttributeError, IndexError, TypeError, ValueError) as e:
        log(
            "WARNING",
            f"Failed to read tire wear for position {tire_position}: {e}",
            category="stint_tracker",
            action="get_tire_wear",
        )
        return 0.0
