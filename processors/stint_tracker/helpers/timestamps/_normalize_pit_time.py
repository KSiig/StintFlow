"""Utilities to normalise pit end timestamps for deduplication.

This module provides a single function, ``_normalize_pit_time``, which
converts an ``HH:MM:SS`` string into a bucketed time (also ``HH:MM:SS``)
using a configurable window size in seconds. The function returns ``None``
when parsing fails or invalid parameters are supplied.
"""

from typing import Any

from ._hhmmss_to_seconds import _hhmmss_to_seconds
from ._seconds_to_hhmmss import _seconds_to_hhmmss


def _normalize_pit_time(pit_end_time: str, window_seconds: int = 10) -> str | None:
    """Return the bucketed HH:MM:SS string for `pit_end_time`.

    Args:
        pit_end_time: time in ``HH:MM:SS`` format.
        window_seconds: positive integer bucket size in seconds.

    Returns:
        A normalized ``HH:MM:SS`` string representing the start of the
        bucket the original time falls into, or ``None`` if input is
        invalid.
    """
    if not isinstance(window_seconds, int) or window_seconds <= 0:
        return None

    try:
        total = _hhmmss_to_seconds(pit_end_time)
    except ValueError:
        return None

    bucket_start = (total // window_seconds) * window_seconds
    return _seconds_to_hhmmss(bucket_start)
