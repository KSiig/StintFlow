"""Provide a canonical empty tyre-state used on telemetry errors.

Returns a complete mapping for all tyre positions with safe, zero-filled
values. Using a single function keeps the "one function per file" pattern
and centralises the default structure used across the tracker.
"""

from typing import Dict

from .constants import TIRE_POSITIONS


def _get_empty_tire_state() -> Dict[str, Dict[str, object]]:
    """Return an empty tyre-state mapping for all canonical positions.

    The returned mapping contains four entries ("fl","fr","rl","rr").
    Each entry is a dict with keys: ``wear``, ``flat``, ``detached``, and
    ``compound`` with safe default values.
    """
    return {
        pos: {"wear": 0.0, "flat": 0, "detached": 0, "compound": "Unknown"}
        for pos in TIRE_POSITIONS
    }