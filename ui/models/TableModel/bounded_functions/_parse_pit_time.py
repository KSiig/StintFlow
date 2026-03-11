"""Utility to parse pit stop times into sortable datetime objects."""

from datetime import datetime
from core.errors import log, log_exception


def _parse_pit_time(self, stint: dict) -> datetime:
    """Parse a stint pit end time into a sortable datetime value."""
    pit_time_str = stint.get("pit_end_time") or "00:00:00"

    if not isinstance(pit_time_str, str):
        log(
            "WARNING",
            f"Invalid pit_end_time type: {type(pit_time_str)}; defaulting to '00:00:00'",
            category="ui",
            action="parse_pit_time",
        )
        pit_time_str = "00:00:00"

    try:
        pit_time = datetime.strptime(pit_time_str, "%H:%M:%S").time()
    except (ValueError, TypeError) as e:
        log_exception(
            e,
            f"Failed to parse pit_end_time: {pit_time_str} for stint: {stint}",
            category="ui",
            action="parse_pit_time",
        )
        pit_time = datetime.strptime("00:00:00", "%H:%M:%S").time()

    return datetime.combine(datetime.min, pit_time)
