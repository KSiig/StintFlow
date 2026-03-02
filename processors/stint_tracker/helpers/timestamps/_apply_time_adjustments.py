"""Helpers for applying HH:MM:SS time adjustments.

This module contains a single function used to apply optional start and
offset adjustments (expressed as ``HH:MM:SS`` strings) to a base seconds
value. The function is intentionally small and raises ``ValueError`` when
time strings are malformed so callers can decide how to handle it.
"""

from typing import Any

from ._hhmmss_to_seconds import _hhmmss_to_seconds


def _apply_time_adjustments(base_seconds: int, start_time: str | None = None, offset_time: str | None = None) -> int:
    """Apply optional ``start_time`` (subtract) and ``offset_time`` (add).

    Args:
        base_seconds: initial number of seconds
        start_time: HH:MM:SS string to subtract from the base (or None)
        offset_time: HH:MM:SS string to add to the base (or None)

    Returns:
        Adjusted seconds as an integer. The function does not clamp the
        result; callers should clamp to zero when appropriate.

    Raises:
        ValueError: if either time string is malformed.
    """
    seconds = int(base_seconds)

    if start_time:
        try:
            seconds -= _hhmmss_to_seconds(start_time)
        except ValueError as e:
            raise ValueError(f"Invalid start_time '{start_time}': {e}") from e

    if offset_time:
        try:
            seconds += _hhmmss_to_seconds(offset_time)
        except ValueError as e:
            raise ValueError(f"Invalid offset_time '{offset_time}': {e}") from e

    return int(seconds)