"""Calculate stint duration between two times with rollover handling."""

from datetime import date, datetime, timedelta

from .normalize_24h_time import normalize_24h_time


def calculate_stint_time(start_time: str, end_time: str) -> timedelta:
    """Return the duration from ``start_time`` to ``end_time`` accounting for day rollover."""
    t1 = datetime.strptime(normalize_24h_time(start_time), "%H:%M:%S").time()
    t2 = datetime.strptime(end_time, "%H:%M:%S").time()

    dt1 = datetime.combine(date.today(), t1)
    dt2 = datetime.combine(date.today(), t2)

    if dt1 < dt2:
        dt1 += timedelta(days=1)

    return dt1 - dt2
