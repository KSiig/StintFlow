"""
Get tire compound from management data.

Retrieves tire compound type for each wheel position.
"""

from typing import Any
from core.errors import log
from .constants import TIRE_INDEX_MAP, COMPOUND_MAP, TIRE_POSITIONS


def get_tire_compound(tire_position: str, tire_mgmt_data: Any = None) -> str:
    """
    Get tire compound for a specific wheel position.
    
    Args:
        tire_position: Tire position ("fl", "fr", "rl", "rr")
        tire_mgmt_data: LMU tire management data
        
    Returns:
        Tire compound name (e.g., "Medium", "Wet")
        Returns "Unknown" if data not available
    """
    # Validate tire position
    if tire_position not in TIRE_POSITIONS:
        log('WARNING', f'Invalid tire position: {tire_position}',
            category='stint_tracker', action='get_tire_compound')
        return "Unknown"
    
    if not tire_mgmt_data:
        log('DEBUG', 'No tire management data provided',
            category='stint_tracker', action='get_tire_compound')
        return "Unknown"
    
    try:
        # Get wheel index from tire position
        wheel_index = TIRE_INDEX_MAP[tire_position]
        
        # Access tire management data structure with granular error handling
        try:
            wheel_info = tire_mgmt_data['wheelInfo']
        except (KeyError, TypeError) as e:
            log('WARNING', f'Missing wheelInfo in tire management data: {str(e)}',
                category='stint_tracker', action='get_tire_compound')
            return "Unknown"
        
        try:
            wheel_locs = wheel_info['wheelLocs']
        except (KeyError, TypeError) as e:
            log('WARNING', f'Missing wheelLocs in tire management data: {str(e)}',
                category='stint_tracker', action='get_tire_compound')
            return "Unknown"
        
        try:
            wheel_data = wheel_locs[wheel_index]
        except (IndexError, TypeError) as e:
            log('WARNING', f'Invalid wheel index {wheel_index}: {str(e)}',
                category='stint_tracker', action='get_tire_compound')
            return "Unknown"
        
        try:
            compound_index = wheel_data['compound']
        except (KeyError, TypeError) as e:
            log('WARNING', f'Missing compound data for wheel {wheel_index}: {str(e)}',
                category='stint_tracker', action='get_tire_compound')
            return "Unknown"
        
        # Convert compound index to name
        compound_name = COMPOUND_MAP.get(compound_index)
        if compound_name is None:
            log('WARNING', f'Unknown compound index: {compound_index}',
                category='stint_tracker', action='get_tire_compound')
            return "Unknown"
        
        return compound_name
        
    except Exception as e:
        log('ERROR', f'Unexpected error getting tire compound: {str(e)}',
            category='stint_tracker', action='get_tire_compound')
        return "Unknown"
