"""Retrieve tyre compound name from LMU tire-management payload.

The function returns a human-friendly compound string (e.g. "Medium").
When data is missing or malformed the function logs a warning and
returns the literal "Unknown".
"""

from typing import Any, Mapping

from core.errors import log
from .constants import TIRE_INDEX_MAP, COMPOUND_MAP, TIRE_POSITIONS
from ._wheel_data_from_mgmt import _wheel_data_from_mgmt

# Logging metadata
_LOG_CATEGORY = "stint_tracker"
_LOG_ACTION = "get_tire_compound"


def _get_tire_compound(tire_position: str, tire_mgmt_data: Mapping[str, Any] | None = None) -> str:
    """Return the compound name for `tire_position` from `tire_mgmt_data`.

    Args:
        tire_position: One of the codes in `TIRE_POSITIONS` ("fl","fr","rl","rr").
        tire_mgmt_data: Expected LMU-style mapping containing `wheelInfo` ->
            `wheelLocs`, a sequence indexed by wheel order.

    Returns:
        A compound name from `COMPOUND_MAP` or the string "Unknown" when
        information is missing or invalid.
    """
    if tire_position not in TIRE_POSITIONS:
        log("WARNING", f"Invalid tire position: {tire_position}",
            category=_LOG_CATEGORY, action=_LOG_ACTION)
        return "Unknown"

    if not tire_mgmt_data:
        log("DEBUG", "No tire management data provided",
            category=_LOG_CATEGORY, action=_LOG_ACTION)
        return "Unknown"

    try:
        wheel_index = TIRE_INDEX_MAP[tire_position]


        wheel_data = _wheel_data_from_mgmt(tire_mgmt_data, wheel_index)
        compound_index = wheel_data.get("compound")
        if compound_index is None:
            raise KeyError("compound missing for wheel")

        compound_name = COMPOUND_MAP.get(compound_index)
        if compound_name is None:
            log("WARNING", f"Unknown compound index: {compound_index}",
                category=_LOG_CATEGORY, action=_LOG_ACTION)
            return "Unknown"

        return compound_name

    except KeyError as e:
        log(
            "WARNING",
            f"Missing or malformed tire management data: {e}",
            category=_LOG_CATEGORY,
            action=_LOG_ACTION,
        )
        return "Unknown"
    except IndexError as e:
        log(
            "WARNING",
            f"Invalid wheel index access: {e}",
            category=_LOG_CATEGORY,
            action=_LOG_ACTION,
        )
        return "Unknown"
    except Exception as e:  # unexpected
        log(
            "ERROR",
            f"Unexpected error getting tire compound: {e}",
            category=_LOG_CATEGORY,
            action=_LOG_ACTION,
        )
        return "Unknown"
