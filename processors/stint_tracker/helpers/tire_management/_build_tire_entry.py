"""Build a single tyre-state entry from player telemetry.

This module provides a single function, `_build_tire_entry`, which extracts
wear, flat, detached and compound information for a specific tyre position.
It returns a safe default entry and logs a warning when data is missing or
malformed.
"""

from typing import Any, Dict, Mapping

from core.errors import log

from ._get_tire_wear import _get_tire_wear
from ._get_tire_compound import _get_tire_compound
from .constants import TIRE_INDEX_MAP

# Centralised log metadata
_LOG_CATEGORY = "stint_tracker"
_LOG_ACTION = "get_tire_state"

TyreData = Mapping[str, Any]

_DEFAULT_ENTRY: Dict[str, object] = {"wear": 0.0, "flat": 0, "detached": 0, "compound": "Unknown"}


def _build_tire_entry(player_vehicle: Any, tire_pos: str, tire_mgmt_data: TyreData) -> Dict[str, object]:
    """Return a dict for `tire_pos` containing wear/flat/detached/compound.

    The function is defensive: invalid `tire_pos`, missing attributes on the
    telemetry object, or indexing errors all result in a logged warning and
    the safe default entry being returned.
    """
    try:
        wheel_idx = TIRE_INDEX_MAP[tire_pos]
    except KeyError:
        log("WARNING", f"Unknown tire position requested: {tire_pos}",
            category=_LOG_CATEGORY, action=_LOG_ACTION)
        return dict(_DEFAULT_ENTRY)

    # Read wheels and index safely
    try:
        wheels = getattr(player_vehicle, "mWheels")
        wheel = wheels[wheel_idx]
    except (AttributeError, IndexError, TypeError) as e:
        log("WARNING", f"Failed to access wheel for {tire_pos}: {e}",
            category=_LOG_CATEGORY, action=_LOG_ACTION)
        return dict(_DEFAULT_ENTRY)

    try:
        return {
            "wear": _get_tire_wear(player_vehicle, tire_pos),
            "flat": getattr(wheel, "mFlat", 0),
            "detached": getattr(wheel, "mDetached", 0),
            "compound": _get_tire_compound(tire_pos, tire_mgmt_data),
        }
    except Exception as e:  # defensive fallback for unforeseen errors
        log("WARNING", f"Failed to build tire entry for {tire_pos}: {e}",
            category=_LOG_CATEGORY, action=_LOG_ACTION)
        return dict(_DEFAULT_ENTRY)