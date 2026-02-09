"""
Stint Tracker Processor.

Independent process that monitors LMU shared memory and creates stint records
when pit stops are detected.

Directory Structure:
-------------------
run.py              - Main entry point (run as separate OS process)
core/               - Core tracking logic (session loop, stint creation, time calc)
pit_detection/      - Pit state detection and player vehicle finding
tire_management/    - Tire wear, compound detection, and change tracking

Usage:
------
python run.py --session-id <id> --drivers <names> [--practice]

The process runs continuously, monitoring game state and reporting events
back to the UI via stdout using the __event__ format.
"""

from .core import track_session, create_stint, calculate_remaining_time
from .pit_detection import PitState, get_pit_state, is_in_garage, find_player_scoring_vehicle
from .tire_management import get_tire_state, get_tire_wear, get_tire_compound, detect_tire_changes

__all__ = [
    # Core
    'track_session',
    'create_stint',
    'calculate_remaining_time',
    
    # Pit detection
    'PitState',
    'get_pit_state',
    'is_in_garage',
    'find_player_scoring_vehicle',
    
    # Tire management
    'get_tire_state',
    'get_tire_wear',
    'get_tire_compound',
    'detect_tire_changes'
]
