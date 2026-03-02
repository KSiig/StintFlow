from ._find_player_scoring_vehicle import _find_player_scoring_vehicle
from typing import Any, Tuple, List

def _get_player_info(
    lmu_telemetry: Any, lmu_scoring: Any, drivers: List[str]
) -> Tuple[Any, Any, str] | None:
    """Return a tuple of (player_vehicle, player_scoring, driver_name).

    Returns ``None`` when player or scoring information cannot be retrieved.
    """
    try:
        player_idx = lmu_telemetry.playerVehicleIdx
        player_vehicle = lmu_telemetry.telemInfo[player_idx]
    except Exception:
        return None

    player_scoring_tuple = _find_player_scoring_vehicle(
        lmu_telemetry, lmu_scoring, drivers
    )
    if not player_scoring_tuple:
        return None

    player_scoring, driver_name = player_scoring_tuple
    return player_vehicle, player_scoring, driver_name