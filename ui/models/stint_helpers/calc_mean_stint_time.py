"""Calculate mean stint duration."""

from datetime import timedelta


def calc_mean_stint_time(stint_times: list[timedelta]) -> timedelta:
    """Return the average of supplied stint durations."""
    if not stint_times:
        return timedelta(0)

    total = sum(stint_times, timedelta(0))
    return total / len(stint_times)
