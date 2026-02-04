"""
Find player's scoring vehicle from driver list.

Matches player vehicle against known driver names.
"""

from typing import Any, Optional
from core.errors import log


def find_player_scoring_vehicle(
    lmu_telemetry: Any,
    lmu_scoring: Any,
    drivers: list[str]
) -> Optional[tuple[Any, str]]:
    """
    Find the scoring vehicle for the player.
    
    Searches through active vehicles in the session to find one matching
    the known driver names. Matching is case-insensitive with whitespace trimmed.
    
    Args:
        lmu_telemetry: LMU telemetry data object
        lmu_scoring: LMU scoring data object  
        drivers: List of known driver names
        
    Returns:
        Tuple of (vehicle, driver_name) if found, None otherwise
    """
    # Validate inputs
    if not drivers:
        log('ERROR', 'Empty drivers list provided',
            category='stint_tracker', action='find_player')
        return None
    
    # Validate active vehicles count
    active_vehicles = lmu_telemetry.activeVehicles
    if active_vehicles <= 0:
        log('WARNING', 'No active vehicles in session',
            category='stint_tracker', action='find_player')
        return None
    
    # Normalize driver names for comparison (case-insensitive, trimmed)
    normalized_drivers = [d.strip().lower() for d in drivers]
    
    # Loop through active vehicles only
    for i in range(active_vehicles):
        vehicle = lmu_scoring.vehScoringInfo[i]
        
        try:
            driver_name = vehicle.mDriverName.decode('utf-8').strip()
        except (UnicodeDecodeError, AttributeError) as e:
            log('WARNING', f'Failed to decode driver name at index {i}: {str(e)}',
                category='stint_tracker', action='find_player')
            continue
        
        # Case-insensitive match
        if driver_name.lower() in normalized_drivers:
            log('DEBUG', f'Found player vehicle for driver: {driver_name}',
                category='stint_tracker', action='find_player')
            return vehicle, driver_name
    
    log('WARNING', f'No matching driver found in: {drivers}',
        category='stint_tracker', action='find_player')
    return None
