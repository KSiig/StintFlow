"""helpers.pit_functions._find_player_scoring_vehicle

Locate the player's scoring vehicle by matching known driver names
against the session scoring information.

This module keeps a single public function (prefixed with an underscore
to indicate internal use) and a small decoding helper to make the
main routine easier to read and test.
"""

from typing import Any, Tuple, List

from core.errors import log, log_exception

from ._decode_driver_name import _decode_driver_name


# Logging metadata constants to avoid repeated literals
_LOG_CATEGORY = 'stint_tracker'
_LOG_ACTION = 'find_player'


def _find_player_scoring_vehicle(
    lmu_telemetry: Any,
    lmu_scoring: Any,
    drivers: List[str]
) -> Tuple[Any, str] | None:
    """Find the scoring vehicle and matching driver name for the player.

    Arguments:
        lmu_telemetry: LMU telemetry data containing `activeVehicles`.
        lmu_scoring: LMU scoring data containing `vehScoringInfo`.
        drivers: List of known driver names to match against.

    Returns:
        A tuple ``(vehicle, driver_name)`` when a match is found, otherwise
        ``None``.
    """

    if not drivers:
        log('ERROR', 'Empty drivers list provided',
            category=_LOG_CATEGORY, action=_LOG_ACTION)
        return None

    # Normalize provided driver names for quick lookups
    normalized: set[str] = {d.strip().lower() for d in drivers if d}
    if not normalized:
        log('ERROR', 'Drivers list contained only empty names',
            category=_LOG_CATEGORY, action=_LOG_ACTION)
        return None

    # Guard access to telemetry and scoring structures
    active_vehicles = getattr(lmu_telemetry, 'activeVehicles', 0) or 0
    if active_vehicles <= 0:
        log('WARNING', 'No active vehicles in session',
            category=_LOG_CATEGORY, action=_LOG_ACTION)
        return None

    veh_list = getattr(lmu_scoring, 'vehScoringInfo', None)
    if not veh_list:
        log('WARNING', 'Scoring vehicle list unavailable',
            category=_LOG_CATEGORY, action=_LOG_ACTION)
        return None

    # Iterate only through the active portion of the scoring list
    for i, vehicle in enumerate(veh_list[:active_vehicles]):
        driver_name = _decode_driver_name(vehicle, i)
        if not driver_name:
            continue

        if driver_name.lower() in normalized:
            log('DEBUG', f'Found player vehicle for driver: {driver_name}',
                category=_LOG_CATEGORY, action=_LOG_ACTION)
            return vehicle, driver_name

    log('WARNING', f'No matching driver found for: {drivers}',
        category=_LOG_CATEGORY, action=_LOG_ACTION)
    return None
