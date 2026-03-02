"""Convert database stint documents into table rows."""

from datetime import timedelta

from ..stint_helpers import calc_mean_stint_time
from ..table_constants import TableRow
from .generate_pending_stints import generate_pending_stints
from .process_completed_stints import process_completed_stints


def convert_stints_to_table(
    stints: list[dict],
    starting_tires: str,
    race_length: str,
    count_tire_changes_fn,
    start_time: str
) -> tuple[list[TableRow], timedelta, int]:
    """Convert stint documents to table row format."""
    if not stints:
        return [], timedelta(0), 0

    rows, tires_left, stint_times, last_tire_change, prev_time_of_day, prev_stint_time = process_completed_stints(
        stints, starting_tires, race_length, count_tire_changes_fn, start_time
    )

    mean_stint_time = calc_mean_stint_time(stint_times)

    if stint_times:
        generate_pending_stints(rows, mean_stint_time, tires_left, prev_time_of_day, prev_stint_time)

    return rows, mean_stint_time, last_tire_change
