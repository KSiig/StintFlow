"""Timestamp helpers used by the stint-tracker processor.

Provides a curated set of small utilities for parsing and normalising
time values used throughout the tracker.
"""

# Conversion helpers
from ._hhmmss_to_seconds import _hhmmss_to_seconds
from ._seconds_to_hhmmss import _seconds_to_hhmmss

# Higher-level utilities
from ._normalize_pit_time import _normalize_pit_time
from ._calculate_remaining_time import _calculate_remaining_time
from ._get_practice_baseline_time import _get_practice_baseline_time
from ._apply_time_adjustments import _apply_time_adjustments

__all__ = (
    "_hhmmss_to_seconds",
    "_seconds_to_hhmmss",
    "_normalize_pit_time",
    "_calculate_remaining_time",
    "_get_practice_baseline_time",
    "_apply_time_adjustments",
)