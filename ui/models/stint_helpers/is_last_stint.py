"""Detect whether another stint would cross midnight."""

from datetime import date, datetime, timedelta


def is_last_stint(pit_end_time: str, mean_stint: timedelta) -> bool:
    """Return True if subtracting ``mean_stint`` would roll into the previous day."""
    t1 = datetime.strptime(pit_end_time, "%H:%M:%S").time()
    dt1 = datetime.combine(date.today(), t1)

    if isinstance(mean_stint, timedelta):
        result = dt1 - mean_stint
        return result.date() < dt1.date()

    dt2 = datetime.combine(date.today(), mean_stint)
    stint_time = dt1 - dt2
    return str(stint_time).startswith("-1 day")
