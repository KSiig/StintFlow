"""
Create stint record in database.

Builds stint document from game state and inserts into MongoDB.
"""

from typing import Any
from bson import ObjectId
from core.database import upsert_official_stint
from core.errors import log, log_exception
from ..tire_management import get_tire_state, detect_tire_changes
from ..tire_management.constants import TIRE_POSITIONS
from .normalize_pit_time import normalize_pit_time


def create_stint(
    remaining_time: str,
    player_vehicle: Any,
    player_scoring: Any,
    num_penalties: int,
    session_id: str,
    driver_name: str,
    tires_coming_in: dict
) -> str | None:
    """
    Create a stint record in the database.
    
    Args:
        remaining_time: Pit end time in HH:MM:SS format
        
        LMU game data:
        player_vehicle: LMU player vehicle telemetry data
        player_scoring: LMU player vehicle scoring data
        num_penalties: Number of penalties before pit stop (for penalty detection)
        
        Session context:
        session_id: Database session ID (must be valid ObjectId string)
        driver_name: Name of the driver completing this stint
        
        Tire data:
        tires_coming_in: Tire state when entering pits
        
    Returns:
        Stint ID if successfully created, None if skipped or failed
    """
    try:
        # Validate session_id is a valid ObjectId
        if not ObjectId.is_valid(session_id):
            log('ERROR', f'Invalid session_id format: {session_id}',
                category='stint_tracker', action='create_stint')
            return None
        
        # Check if penalty was served (don't record penalty laps)
        # When a penalty is served, the penalty count decreases
        # So: num_penalties (before) > mNumPenalties (after) means penalty was served
        is_penalty_served = num_penalties > player_scoring.mNumPenalties
        
        if is_penalty_served:
            log('INFO', 'Penalty served - skipping stint creation',
                category='stint_tracker', action='create_stint')
            return None
        
        # Get outgoing tire state
        tires_outgoing = get_tire_state(player_vehicle)
        
        # Build tire data with change detection
        tire_data = {}
        for tire in TIRE_POSITIONS:
            tire_data[tire] = {
                "incoming": tires_coming_in.get(tire, {}),
                "outgoing": tires_outgoing[tire]
            }
        
        tire_data['tires_changed'] = detect_tire_changes(tires_outgoing)
        
        # Normalize pit end time for dedupe across multiple trackers
        normalized_time = normalize_pit_time(remaining_time)
        if not normalized_time:
            log('WARNING', f'Invalid pit end time format: {remaining_time}',
                category='stint_tracker', action='create_stint')
            normalized_time = remaining_time

        stint_key = f'{session_id}:{normalized_time}'

        # Build stint document
        stint = {
            "session_id": ObjectId(session_id),
            "driver": driver_name,
            "pit_end_time": remaining_time,
            "pit_end_time_bucket": normalized_time,
            "stint_key": stint_key,
            "official": True,
            "tire_data": tire_data
        }

        stint_id, was_inserted = upsert_official_stint(stint, stint_key)

        if not stint_id:
            return None

        if was_inserted:
            log('INFO', f'Created stint {stint_id} for driver {driver_name}',
                category='stint_tracker', action='create_stint')
        else:
            log('INFO', f'Deduped stint {stint_id} for driver {driver_name}',
                category='stint_tracker', action='create_stint')

        return stint_id
        
    except Exception as e:
        log_exception(e, 'Failed to create stint',
                     category='stint_tracker', action='create_stint')
        return None
