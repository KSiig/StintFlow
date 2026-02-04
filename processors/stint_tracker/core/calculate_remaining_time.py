"""
Calculate remaining race time.

Converts LMU scoring data to HH:MM:SS format for stint tracking.
"""

import math
from typing import Any, Optional
from core.errors import log


def calculate_remaining_time(
    lmu_scoring: Any,
    start_time: Optional[str] = None,
    offset_time: Optional[str] = None
) -> str:
    """
    Calculate remaining time from LMU scoring data.
    
    Args:
        lmu_scoring: LMU scoring data object
        start_time: Start time to subtract from remaining time (HH:MM:SS)
                   Used when tracking partial stints
        offset_time: Time offset to add to remaining time (HH:MM:SS)
                    Used for timing adjustments
        
    Returns:
        Remaining time in HH:MM:SS format
        
    Raises:
        ValueError: If time strings are malformed
        AttributeError: If scoring data is invalid
    """
    # Validate scoring data exists
    if not lmu_scoring or not hasattr(lmu_scoring, 'scoringInfo'):
        log('ERROR', 'Invalid scoring data provided',
            category='stint_tracker', action='calculate_remaining_time')
        return "00:00:00"
    
    scoring_info = lmu_scoring.scoringInfo
    
    # Calculate base remaining time from race clock
    # mEndET = race end time, mCurrentET = current elapsed time
    remaining_seconds = math.ceil(scoring_info.mEndET - scoring_info.mCurrentET)
    
    # Apply time adjustments if provided
    # start_time: subtracted when measuring from a specific point in the stint
    # offset_time: added when adjusting for delays or time corrections
    if start_time or offset_time:
        if start_time:
            remaining_seconds -= hhmmss_to_seconds(start_time)
        if offset_time:
            remaining_seconds += hhmmss_to_seconds(offset_time)
    
    return seconds_to_hhmmss(remaining_seconds)


def hhmmss_to_seconds(time_str: str) -> int:
    """
    Convert HH:MM:SS string to total seconds.
    
    Args:
        time_str: Time in HH:MM:SS format
        
    Returns:
        Total seconds as integer
        
    Raises:
        ValueError: If time_str format is invalid
    """
    try:
        parts = time_str.split(":")
        if len(parts) != 3:
            raise ValueError(f"Expected HH:MM:SS format, got: {time_str}")
        
        h, m, s = map(int, parts)
        
        # Validate ranges
        if m < 0 or m >= 60 or s < 0 or s >= 60:
            raise ValueError(f"Invalid time values in: {time_str}")
        
        return h * 3600 + m * 60 + s
        
    except (ValueError, AttributeError) as e:
        log('ERROR', f'Invalid time format "{time_str}": {str(e)}',
            category='stint_tracker', action='hhmmss_to_seconds')
        raise ValueError(f"Invalid time format: {time_str}") from e


def seconds_to_hhmmss(seconds: int) -> str:
    """
    Convert seconds to HH:MM:SS format.
    
    Args:
        seconds: Total seconds (negative values clamped to 0)
        
    Returns:
        Time string in HH:MM:SS format with zero-padded values
    """
    seconds = max(0, seconds)  # Clamp negative time to 0:00:00
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    return f"{h:02}:{m:02}:{s:02}"
