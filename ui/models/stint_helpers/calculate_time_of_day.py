"""Advance a time-of-day marker by a stint duration."""

from datetime import date, datetime, timedelta


def calculate_time_of_day(prev_time_of_day, prev_stint_time: timedelta) -> str:
    """Return next time-of-day string after adding ``prev_stint_time``."""
    if isinstance(prev_time_of_day, str):
        prev_time_of_day = datetime.strptime(prev_time_of_day, "%H:%M:%S").time()

    if isinstance(prev_time_of_day, datetime):
        dt = prev_time_of_day
    else:
        dt = datetime.combine(date.today(), prev_time_of_day)

    new_dt = dt + prev_stint_time
    return new_dt.time().strftime("%H:%M:%S")
