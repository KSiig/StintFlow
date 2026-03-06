from __future__ import annotations

from datetime import timedelta


def format_stint_time(stint_time) -> str:
    """Return an HH:MM:SS string for the provided stint time value."""
    if isinstance(stint_time, timedelta):
        return str(stint_time).split('.', 1)[0]

    if isinstance(stint_time, str):
        return stint_time.split('.', 1)[0]

    try:
        total_seconds = int(float(stint_time))
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    except Exception:
        return str(stint_time)
