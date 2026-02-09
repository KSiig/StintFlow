"""
Get complete tire state from vehicle.

Extracts wear, damage, and compound information for all four tires.
"""

from typing import Any, Optional
from core.errors import log, log_exception
from .get_tire_wear import get_tire_wear
from .get_tire_compound import get_tire_compound
from .constants import TIRE_INDEX_MAP
import requests


def get_tire_state(player_vehicle: Any) -> dict:
    """
    Get complete state of all tires.
    
    Args:
        player_vehicle: LMU player vehicle telemetry object
        
    Returns:
        Dictionary with tire data for each position (fl, fr, rl, rr):
        {
            "fl": {
                "wear": float,
                "flat": int,
                "detached": int,
                "compound": str
            },
            ...
        }
    """
    tire_mgmt_data = _get_tire_management_data()
    
    tire_state = {}
    
    try:
        # Validate mWheels exists and has correct length
        if not hasattr(player_vehicle, 'mWheels'):
            log('ERROR', 'Player vehicle missing mWheels attribute',
                category='stint_tracker', action='get_tire_state')
            return _get_empty_tire_state()
        
        if len(player_vehicle.mWheels) < 4:
            log('ERROR', f'mWheels has insufficient elements: {len(player_vehicle.mWheels)}',
                category='stint_tracker', action='get_tire_state')
            return _get_empty_tire_state()
        
        for tire_pos, wheel_idx in TIRE_INDEX_MAP.items():
            try:
                wheel = player_vehicle.mWheels[wheel_idx]
                
                tire_state[tire_pos] = {
                    "wear": get_tire_wear(player_vehicle, tire_pos),
                    "flat": wheel.mFlat,
                    "detached": wheel.mDetached,
                    "compound": get_tire_compound(tire_pos, tire_mgmt_data)
                }
            except (IndexError, AttributeError) as e:
                log('WARNING', f'Failed to get state for tire {tire_pos}: {str(e)}',
                    category='stint_tracker', action='get_tire_state')
                tire_state[tire_pos] = {
                    "wear": 0.0,
                    "flat": 0,
                    "detached": 0,
                    "compound": "Unknown"
                }
    
    except Exception as e:
        log_exception(e, 'Unexpected error getting tire state',
                     category='stint_tracker', action='get_tire_state')
        return _get_empty_tire_state()
    
    return tire_state


def _get_empty_tire_state() -> dict:
    """
    Get empty tire state structure for error cases.
    
    Returns:
        Dictionary with default values for all tire positions
    """
    return {
        tire_pos: {
            "wear": 0.0,
            "flat": 0,
            "detached": 0,
            "compound": "Unknown"
        }
        for tire_pos in TIRE_INDEX_MAP.keys()
    }


def _get_tire_management_data() -> Optional[Any]:
    """
    Get tire management data from LMU REST API.
    
    Connects to LMU's local REST API to retrieve tire management
    information including compound data.
    
    Returns:
        Tire management data object or None if retrieval fails
    """
    try:
        url = "http://localhost:6397/rest/garage/UIScreen/TireManagement"
        headers = {
            "accept": "application/json",
        }

        response = requests.get(url, headers=headers, timeout=2)
        response.raise_for_status()

        log('DEBUG', 'Successfully retrieved tire management data',
            category='stint_tracker', action='get_tire_management_data')
        return response.json()
        
    except requests.RequestException as e:
        log('WARNING', f'Failed to retrieve tire management data: {str(e)}',
            category='stint_tracker', action='get_tire_management_data')
        return None
    except Exception as e:
        log_exception(e, 'Unexpected error retrieving tire management data',
                     category='stint_tracker', action='get_tire_management_data')
        return None
