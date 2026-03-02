"""Calculate remaining race time from LMU scoring data.

This helper converts LMU scoring values into an ``HH:MM:SS`` string used
by the stint tracker. It is defensive: invalid scoring input or malformed
time strings are logged and the function returns the zero-time string.
"""

import math
from typing import Any

from core.errors import log, log_exception
from ._seconds_to_hhmmss import _seconds_to_hhmmss
from ._apply_time_adjustments import _apply_time_adjustments


def _calculate_remaining_time(lmu_scoring: Any, start_time: str = None, offset_time: str = None) -> str:
    """Return remaining race time as an ``HH:MM:SS`` string.

    Args:
        lmu_scoring: LMU scoring data object with a ``scoringInfo`` attribute
            exposing numeric ``mEndET`` and ``mCurrentET`` values.
        start_time: optional ``HH:MM:SS`` to subtract (partial-stint start)
        offset_time: optional ``HH:MM:SS`` to add (timing corrections)

    Returns:
        Normalised remaining time string. On errors returns "00:00:00".
    """
    try:
        if not lmu_scoring or not hasattr(lmu_scoring, "scoringInfo"):
            log("ERROR", "Invalid scoring data provided",
                category="stint_tracker", action="calculate_remaining_time")
            return "00:00:00"

        scoring_info = lmu_scoring.scoringInfo

        # base remaining seconds (ceil to avoid fractional seconds)
        base = math.ceil(scoring_info.mEndET - scoring_info.mCurrentET)

        # apply optional adjustments and clamp to zero
        adjusted = _apply_time_adjustments(base, start_time, offset_time)
        adjusted = max(0, int(adjusted))

        return _seconds_to_hhmmss(adjusted)

    except ValueError as e:
        # _hhmmss_to_seconds raises ValueError for malformed strings
        log("WARNING", f"Malformed time string when calculating remaining time: {e}",
            category="stint_tracker", action="calculate_remaining_time")
        return "00:00:00"
    except Exception as e:  # defensive catch-all
        log_exception(e, "Unexpected error calculating remaining time",
                      category="stint_tracker", action="calculate_remaining_time")
        return "00:00:00"


