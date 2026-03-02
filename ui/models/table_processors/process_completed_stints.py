"""Process completed stints into table rows."""

from datetime import timedelta

from ..stint_helpers import (
    calculate_stint_time,
    calculate_time_of_day,
    format_timedelta,
    get_stint_type
)
from ..table_constants import ColumnIndex, TableRow
from ..table_utils import create_table_row


def process_completed_stints(
    stints: list[dict],
    starting_tires: str,
    race_length: str,
    count_tire_changes_fn,
    start_time: str
) -> tuple[list[TableRow], int, list[timedelta], int, str, timedelta]:
    """Process completed stints into table rows and capture summary metadata."""
    rows: list[TableRow] = []
    stint_times: list[timedelta] = []
    prev_pit_time = race_length
    prev_time_of_day = start_time
    prev_stint_time = timedelta(0)
    tires_left = int(starting_tires)
    start_of_stint = 0

    for i, stint in enumerate(stints):
        time_of_day = calculate_time_of_day(prev_time_of_day, prev_stint_time)

        stint_time = calculate_stint_time(prev_pit_time, stint.get("pit_end_time", "00:00:00"))
        if not stint.get("excluded", False):
            stint_times.append(stint_time)

        tire_data = stint.get("tire_data", {})
        total_changed, medium_changed = count_tire_changes_fn(tire_data)
        tires_left -= medium_changed

        stint_amounts = i - start_of_stint
        stint_type = get_stint_type(stint_amounts)

        if total_changed:
            stint_type = "Single" if start_of_stint == i else ""
            start_of_stint = i + 1
        elif stint_amounts and not total_changed:
            if rows:
                rows[start_of_stint][ColumnIndex.STINT_TYPE] = get_stint_type(stint_amounts)
            stint_type = ""

        row = create_table_row(
            stint_type=stint_type,
            driver=stint.get("driver", ""),
            status="Completed",
            pit_time=stint.get("pit_end_time", "00:00:00"),
            tires_changed=total_changed,
            tires_left=tires_left,
            stint_time=format_timedelta(stint_time),
            time_of_day=time_of_day,
        )
        rows.append(row)

        prev_pit_time = stint.get("pit_end_time", "00:00:00")
        prev_time_of_day = time_of_day
        prev_stint_time = stint_time

    last_tire_change = int(rows[-1][ColumnIndex.TIRES_CHANGED]) if rows else 0

    return rows, tires_left, stint_times, last_tire_change, prev_time_of_day, prev_stint_time
