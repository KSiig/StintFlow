"""
Main tracking loop for stint tracker.

Monitors game state and creates stint records when pit stops are detected.
"""

import time
from typing import Any, Optional
from core.errors import log
from core.database import get_stints, get_session, get_event
from ..pit_detection import (
    get_pit_state, PitState, is_in_garage, find_player_scoring_vehicle
)
from ..tire_management import get_tire_state
from .create_stint import create_stint
from .calculate_remaining_time import calculate_remaining_time


# Polling frequency for game state monitoring (Hz)
POLLING_FREQUENCY = 1


def _get_practice_baseline_time(session_id: str) -> Optional[str]:
    """
    Get baseline time for practice mode tracking.
    
    In practice mode, the first stint starts from the event length,
    and subsequent stints start from the previous stint's pit end time.
    
    Args:
        session_id: Database session ID
        
    Returns:
        Baseline time in HH:MM:SS format, or None if not found
    """
    stints = list(get_stints(session_id))
    
    if stints:
        # Use previous stint's pit end time
        return stints[-1]['pit_end_time']
    else:
        # No stints yet - use event length as baseline
        session = get_session(session_id)
        event = get_event(str(session['race_id']))
        return event['length']


def track_session(
    lmu_telemetry: Any,
    lmu_scoring: Any,
    session_id: str,
    drivers: list[str],
    is_practice: bool = False
) -> None:
    """
    Track session and create stints when pit stops are detected.
    
    Args:
        lmu_telemetry: LMU telemetry data object
        lmu_scoring: LMU scoring data object
        session_id: Database session ID
        drivers: List of driver names
        is_practice: Whether this is a practice session
    """
    # State tracking
    pit_stop_in_progress = False
    num_penalties = 0
    garage_time_snapshot = "00:00:00"  # Time when player was last in garage
    tracking_enabled = False  # For practice mode: wait for player to return to garage
    driver_name = ""
    tires_coming_in = {}
    practice_baseline_time = None
    
    # Load baseline time for practice mode
    if is_practice:
        practice_baseline_time = _get_practice_baseline_time(session_id)
        log('DEBUG', f'Practice mode baseline time: {practice_baseline_time}',
            category='stint_tracker', action='track_session')
    
    log('INFO', f'Tracking session {session_id}',
        category='stint_tracker', action='track_session')
    
    # Main tracking loop
    while True:
        # Get player vehicle data
        player_idx = lmu_telemetry.playerVehicleIdx
        player_vehicle = lmu_telemetry.telemInfo[player_idx]
        player_scoring, driver_name = find_player_scoring_vehicle(
            lmu_telemetry, lmu_scoring, drivers
        )
        
        if not player_scoring:
            time.sleep(1 / POLLING_FREQUENCY)
            continue
        
        pit_state = get_pit_state(player_scoring)
        
        # Capture tire state when coming into pits
        if pit_state == PitState.COMING_IN and not pit_stop_in_progress:
            log('DEBUG', f'Driver {driver_name} entering pits',
                category='stint_tracker', action='track_session')
            tires_coming_in = get_tire_state(player_vehicle)
        
        # Practice mode: wait for player to return to garage before tracking
        if is_practice and not tracking_enabled:
            if is_in_garage(player_scoring):
                log('INFO', 'Player in garage - tracking enabled',
                    category='stint_tracker', action='track_session')
                tracking_enabled = True
            else:
                log('INFO', 'Return to garage - tracking disabled',
                    category='stint_tracker', action='track_session')
                time.sleep(1)
                continue
        else:
            tracking_enabled = True
        
        # Track remaining time when in garage
        if is_in_garage(player_scoring):
            print("__info__:stint_tracker:player_in_garage")
            pit_stop_in_progress = True
            garage_time_snapshot = calculate_remaining_time(lmu_scoring)
        
        # Detect pit stop completion
        if not pit_stop_in_progress and pit_state == PitState.LEAVING:
            log('INFO', f'Driver {driver_name} leaving pits - creating stint',
                category='stint_tracker', action='track_session')
            pit_stop_in_progress = True
            
            # Calculate remaining time
            if is_practice and practice_baseline_time:
                # Practice mode: calculate time from baseline with garage offset
                remaining_time = calculate_remaining_time(
                    lmu_scoring,
                    start_time=garage_time_snapshot,
                    offset_time=practice_baseline_time
                )
                log('DEBUG', f'Practice stint time: {remaining_time} (baseline: {practice_baseline_time}, offset: {garage_time_snapshot})',
                    category='stint_tracker', action='track_session')
            else:
                # Race mode: use current race time
                remaining_time = calculate_remaining_time(lmu_scoring)
            
            # Create stint record
            stint_id = create_stint(
                remaining_time=remaining_time,
                player_vehicle=player_vehicle,
                player_scoring=player_scoring,
                num_penalties=num_penalties,
                session_id=session_id,
                driver_name=driver_name,
                tires_coming_in=tires_coming_in
            )
            
            # Update baseline for next practice stint
            if is_practice and stint_id:
                practice_baseline_time = remaining_time
                log('DEBUG', f'Updated practice baseline to: {practice_baseline_time}',
                    category='stint_tracker', action='track_session')
        
        # Reset state when back on track
        if pit_state == PitState.ON_TRACK and pit_stop_in_progress:
            log('DEBUG', f'Driver {driver_name} back on track',
                category='stint_tracker', action='track_session')
            num_penalties = player_scoring.mNumPenalties
            pit_stop_in_progress = False
        
        time.sleep(1 / POLLING_FREQUENCY)
