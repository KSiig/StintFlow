"""Extract full tyre state from a player-vehicle telemetry object.

The module exposes a single function, `_get_tire_state`, which returns a
mapping for the four tyre positions (`fl`, `fr`, `rl`, `rr`) containing
wear, flat, detached and compound information. The function handles
missing or malformed telemetry gracefully and logs useful diagnostics.
"""

from typing import Any, Dict

from core.errors import log, log_exception
from ._get_empty_tire_state import _get_empty_tire_state
from ._get_tire_management_data import _get_tire_management_data
from ._build_tire_entry import _build_tire_entry
from .constants import TIRE_INDEX_MAP


def _get_tire_state(player_vehicle: Any) -> Dict[str, Dict[str, object]]:
    """Return the complete tyre state for `player_vehicle`.

    If the incoming telemetry is missing or malformed the function returns the
    result of `_get_empty_tire_state()` which provides a safe, zero-filled
    structure for all four tyre positions.
    """
    tire_mgmt_data = _get_tire_management_data()

    # Validate presence of wheels early and return a complete empty state on error
    if not hasattr(player_vehicle, 'mWheels'):
        log('ERROR', 'Player vehicle missing mWheels attribute',
            category='stint_tracker', action='get_tire_state')
        return _get_empty_tire_state()

    wheels = getattr(player_vehicle, 'mWheels')
    if not isinstance(wheels, (list, tuple)) or len(wheels) < 4:
        log('ERROR', f'mWheels has insufficient elements: {len(wheels) if hasattr(wheels, "__len__") else "?"}',
            category='stint_tracker', action='get_tire_state')
        return _get_empty_tire_state()

    try:
        result: Dict[str, Dict[str, object]] = {}
        for tire_pos in TIRE_INDEX_MAP.keys():
            result[tire_pos] = _build_tire_entry(player_vehicle, tire_pos, tire_mgmt_data)

        return result
    except Exception as e:
        log_exception(e, 'Unexpected error getting tire state',
                     category='stint_tracker', action='get_tire_state')
        return _get_empty_tire_state()



