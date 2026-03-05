from __future__ import annotations

from datetime import datetime, timedelta, timezone


def _format_ts(value) -> str:
    """Convert stored timestamp values into short local-time display strings."""
    if isinstance(value, datetime):
        timestamp = value
    else:
        try:
            timestamp = datetime.fromisoformat(str(value))
        except Exception:
            return str(value)

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=timezone.utc)

    try:
        timestamp = timestamp.astimezone()
    except Exception:
        pass

    age = datetime.now(timestamp.tzinfo) - timestamp
    if age > timedelta(days=1):
        return timestamp.strftime("%d-%m/%y %H:%M")
    return timestamp.strftime("%H:%M")
