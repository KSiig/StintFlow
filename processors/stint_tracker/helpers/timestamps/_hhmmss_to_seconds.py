"""Timestamp parsing utilities.

Small helper to convert an ``HH:MM:SS`` string into total seconds. The
function logs an error on invalid input and raises ``ValueError`` like the
previous implementation to preserve caller expectations.
"""

from core.errors import log
from typing import Tuple


def _hhmmss_to_seconds(time_str: str) -> int:
    """Convert an ``HH:MM:SS`` time string to total seconds.

    Args:
        time_str: Time in ``HH:MM:SS`` format.

    Returns:
        Total seconds as an integer.

    Raises:
        ValueError: If `time_str` is not a valid HH:MM:SS string.
    """
    try:
        parts: Tuple[str, ...] = tuple(time_str.split(":"))
        if len(parts) != 3:
            raise ValueError(f"Expected HH:MM:SS format, got: {time_str}")

        h, m, s = map(int, parts)

        # Validate ranges
        if h < 0 or m < 0 or m >= 60 or s < 0 or s >= 60:
            raise ValueError(f"Invalid time values in: {time_str}")

        return h * 3600 + m * 60 + s

    except (ValueError, AttributeError) as e:
        log("ERROR", f"Invalid time format \"{time_str}\": {e}",
            category="stint_tracker", action="hhmmss_to_seconds")
        raise ValueError(f"Invalid time format: {time_str}") from e
