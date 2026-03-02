"""Format a timedelta as HH:MM:SS."""

from datetime import timedelta


def format_timedelta(td: timedelta) -> str:
    """Return a zero-padded HH:MM:SS string."""
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
