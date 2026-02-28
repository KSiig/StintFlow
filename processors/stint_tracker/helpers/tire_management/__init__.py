"""Tire-management helpers exported for the stint-tracker processor.

This module re-exports a curated set of small helper functions and
constants used by the stint-tracker. Importing from this package gives
callers a single, stable import surface for tyre-related utilities.
"""

# Core helpers
from ._get_tire_state import _get_tire_state
from ._get_tire_wear import _get_tire_wear
from ._get_tire_compound import _get_tire_compound
from ._detect_tire_changes import _detect_tire_changes

# Data helpers
from ._get_tire_management_data import _get_tire_management_data
from ._wheel_data_from_mgmt import _wheel_data_from_mgmt
from ._get_empty_tire_state import _get_empty_tire_state

# Small builders
from ._build_tire_entry import _build_tire_entry

# Constants
from .constants import (
    TIRE_POSITIONS,
    TIRE_INDEX_MAP,
    COMPOUND_MAP,
    WEAR_COMPARISON_EPSILON,
)

__all__ = (
    # core
    "_get_tire_state",
    "_get_tire_wear",
    "_get_tire_compound",
    "_detect_tire_changes",

    # data
    "_get_tire_management_data",
    "_wheel_data_from_mgmt",
    "_get_empty_tire_state",

    # builders
    "_build_tire_entry",

    # constants
    "TIRE_POSITIONS",
    "TIRE_INDEX_MAP",
    "COMPOUND_MAP",
    "WEAR_COMPARISON_EPSILON",
)
