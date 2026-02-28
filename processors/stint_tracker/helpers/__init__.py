"""Helper utilities for the stint-tracker processor.

This package collects small, focused helper functions used throughout the
stint-tracker processor. Instead of using ``from .foo import *`` we expose a
curated set of symbols here so callers can import from
``processors.stint_tracker.helpers`` with predictable names.
"""

# Parser helpers
from .parser import _make_parser, _parse_args

# Agent registration helpers
from .agents import (
    _register_tracker_agent,
    _unregister_tracker_agent,
    _maybe_update_heartbeat,
    _maybe_cleanup_stale_agents,
)

# Tire management helpers + constants
from .tire_management import (
    _get_tire_state,
    _get_tire_wear,
    _get_tire_compound,
    _detect_tire_changes,
    _get_empty_tire_state,
    _get_tire_management_data,
    TIRE_POSITIONS,
    TIRE_INDEX_MAP,
    COMPOUND_MAP,
    WEAR_COMPARISON_EPSILON,
)

# Pit-detection helpers
from .pit_functions import (
  PitState, 
  _get_pit_state, 
  _is_in_garage, 
  _find_player_scoring_vehicle, 
  _decode_driver_name,
   _get_player_info
)

# Timestamp helpers
from .timestamps import (
    _normalize_pit_time,
    _calculate_remaining_time,
    _hhmmss_to_seconds,
    _seconds_to_hhmmss,
    _get_practice_baseline_time,
)

# LMU shared-memory helper
from ._open_lmu_shared_memory import _open_lmu_shared_memory

__all__ = (
    # parser
    "_make_parser",
    "_parse_args",

    # agents
    "_register_tracker_agent",
    "_unregister_tracker_agent",
    "_maybe_update_heartbeat",
    "_maybe_cleanup_stale_agents",

    # tire management
    "_get_tire_state",
    "_get_tire_wear",
    "_get_tire_compound",
    "_detect_tire_changes",
    "_get_empty_tire_state",
    "_get_tire_management_data",
    "TIRE_POSITIONS",
    "TIRE_INDEX_MAP",
    "COMPOUND_MAP",
    "WEAR_COMPARISON_EPSILON",

    # pit detection
    "PitState",
    "_get_pit_state",
    "_is_in_garage",
    "_find_player_scoring_vehicle",
    "_decode_driver_name",
    "_get_player_info",

    # timestamps
    "_normalize_pit_time",
    "_calculate_remaining_time",
    "_hhmmss_to_seconds",
    "_seconds_to_hhmmss",
    "_get_practice_baseline_time",

    # shared memory
    "_open_lmu_shared_memory",
)