"""Convert a timedelta to a time object (mod 24h)."""

from datetime import time, timedelta


def timedelta_to_time(td: timedelta) -> time:
    """Return a ``datetime.time`` derived from ``td`` modulo 24 hours."""
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    hours %= 24
    return time(hour=hours, minute=minutes, second=seconds)
