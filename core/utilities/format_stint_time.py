from __future__ import annotations

from datetime import timedelta


def format_stint_time(stint_time) -> str:
    """Return an HH:MM:SS string for the provided stint time value.

    For ``timedelta`` inputs we normalize by converting to total seconds and
    formatting the hours component explicitly so that durations longer than a
    day still render as ``HH:MM:SS`` rather than Python's default
    ``'1 day, 02:00:00'`` representation.  The numeric branch already uses
    the same approach, so non-``timedelta`` values continue to be handled in
    the same way.
    """
    if isinstance(stint_time, timedelta):
        total_seconds = int(stint_time.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"

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
