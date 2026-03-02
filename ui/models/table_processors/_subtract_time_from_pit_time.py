"""Utility to subtract a timedelta from a pit time string."""

from datetime import datetime, timedelta

from ..stint_helpers import timedelta_to_time


def _subtract_time_from_pit_time(pit_time_str: str, delta: timedelta) -> str:
    """Subtract ``delta`` from ``pit_time_str`` and return an ``HH:MM:SS`` string."""
    pit_time = datetime.strptime(pit_time_str, "%H:%M:%S").time()
    delta_as_time = timedelta_to_time(delta)

    pit_datetime = datetime.combine(datetime.today(), pit_time)
    delta_timedelta = timedelta(
        hours=delta_as_time.hour,
        minutes=delta_as_time.minute,
        seconds=delta_as_time.second,
    )

    result_datetime = pit_datetime - delta_timedelta
    return result_datetime.time().strftime("%H:%M:%S")
