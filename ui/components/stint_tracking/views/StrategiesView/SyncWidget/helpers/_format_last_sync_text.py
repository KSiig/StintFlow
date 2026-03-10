"""Format a strategy's last sync timestamp for display."""

from __future__ import annotations

from datetime import datetime


def _format_last_sync_text(self, last_sync: str) -> str | None:
    """Return a display string for the last sync timestamp, if valid."""
    if not last_sync:
        return None

    try:
        normalized_value = last_sync.replace("Z", "+00:00")
        parsed_timestamp = datetime.fromisoformat(normalized_value)

        # ensure we have a timezone so comparisons to "today" make sense
        local_tz = datetime.now().astimezone().tzinfo
        if parsed_timestamp.tzinfo is None:
            parsed_timestamp = parsed_timestamp.replace(tzinfo=local_tz)
        else:
            parsed_timestamp = parsed_timestamp.astimezone(local_tz)

        # determine whether this timestamp represents a local "today"
        today_local = datetime.now().astimezone(local_tz).date()
        if parsed_timestamp.date() == today_local:
            # only show the time when the sync happened today
            return f"Last sync: {parsed_timestamp.strftime('%H:%M:%S')}"

        # older than today, display with month name and day-ordinal
        day = parsed_timestamp.day
        if 11 <= day <= 13:
            suffix = "th"
        else:
            suffix = {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
        date_str = parsed_timestamp.strftime(f"%B {day}{suffix}")
        return f"Last sync: {date_str} {parsed_timestamp.strftime('%H:%M:%S')}"
    except ValueError:
        return None