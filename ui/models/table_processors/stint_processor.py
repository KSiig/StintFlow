"""
Stint processor for converting database stints to table rows.

Handles processing of completed stints and generation of pending stints
based on mean stint times.
"""

from datetime import datetime, timedelta

from ..table_constants import TableRow, ColumnIndex
from ..table_utils import create_table_row
from ..stint_helpers import (
    get_stint_type,
    calculate_stint_time,
    calculate_time_of_day,
    format_timedelta,
    calc_mean_stint_time,
    timedelta_to_time,
    is_last_stint
)

from ..table_constants import FULL_TIRE_SET, NO_TIRE_CHANGE


def convert_stints_to_table(
    stints: list[dict],
    starting_tires: str,
    race_length: str,
    count_tire_changes_fn,
    start_time: str
) -> tuple[list[TableRow], timedelta, int]:
    """
    Convert stint documents to table row format.
    
    Args:
        stints: List of stint documents from database
        starting_tires: Total tire count at race start
        race_length: Total race length
        count_tire_changes_fn: Function to count tire changes
        start_time: Race start time
        
    Returns:
        List of rows with completed and pending stints
    """
    if not stints:
        return [], timedelta(0), 0
    
    # Process completed stints
    rows, tires_left, stint_times, last_tire_change, prev_time_of_day, prev_stint_time = process_completed_stints(
        stints, starting_tires, race_length, count_tire_changes_fn, start_time
    )
    
    mean_stint_time = calc_mean_stint_time(stint_times)
    
    # Generate pending stints
    if stint_times:
        generate_pending_stints(rows, mean_stint_time, tires_left, prev_time_of_day, prev_stint_time)

    return rows, mean_stint_time, last_tire_change


def process_completed_stints(
    stints: list[dict],
    starting_tires: str,
    race_length: str,
    count_tire_changes_fn,
    start_time: str
) -> tuple[list[TableRow], int, list[timedelta], int, timedelta, timedelta]:
    """
    Process completed stints into table rows.
    
    Args:
        stints: List of stint documents
        starting_tires: Total tire count at start
        race_length: Total race length
        count_tire_changes_fn: Function to count tire changes
        start_time: Race start time

    Returns:
        Tuple of (rows, remaining_tires, stint_times, last_tire_change, prev_time_of_day, prev_stint_time)
    """
    rows = []
    stint_times = []
    prev_pit_time = race_length
    prev_time_of_day = start_time
    prev_stint_time = timedelta(0)
    tires_left = int(starting_tires)
    start_of_stint = 0
    
    for i, stint in enumerate(stints):
        time_of_day = calculate_time_of_day(prev_time_of_day, prev_stint_time)

        # Calculate stint duration
        stint_time = calculate_stint_time(prev_pit_time, stint.get('pit_end_time', '00:00:00'))
        # Only include this stint in mean calculation if it's not marked excluded
        if not stint.get('excluded', False):
            stint_times.append(stint_time)
        
        # Count tire changes
        tire_data = stint.get('tire_data', {})
        total_changed, medium_changed = count_tire_changes_fn(tire_data)
        tires_left -= medium_changed
        
        # Determine stint type
        stint_amounts = i - start_of_stint
        stint_type = get_stint_type(stint_amounts)
        
        if total_changed:
            stint_type = "Single" if start_of_stint == i else ""
            start_of_stint = i + 1
        elif stint_amounts and not total_changed:
            # Multi-stint in progress - update first row, clear current
            if rows:
                rows[start_of_stint][ColumnIndex.STINT_TYPE] = get_stint_type(stint_amounts)
            stint_type = ""
        
        # Add row
        row = create_table_row(
            stint_type=stint_type,
            driver=stint.get("driver", ""),
            status="Completed",
            pit_time=stint.get("pit_end_time", "00:00:00"),
            tires_changed=total_changed,
            tires_left=tires_left,
            stint_time=format_timedelta(stint_time),
            time_of_day=time_of_day
        )
        rows.append(row)
        
        prev_pit_time = stint.get('pit_end_time', '00:00:00')
        prev_time_of_day = time_of_day
        prev_stint_time = stint_time
    
    last_tire_change = int(rows[-1][ColumnIndex.TIRES_CHANGED])

    return rows, tires_left, stint_times, last_tire_change, prev_time_of_day, prev_stint_time


def generate_pending_stints(
    rows: list[TableRow],
    mean_stint_time: timedelta,
    starting_tires_left: int,
    prev_time_of_day: timedelta,
    prev_stint_time: timedelta
) -> None:
    """
    Generate pending stints based on mean stint time.
    
    Stints are created by repeatedly subtracting the average duration from the
    last recorded pit time. The loop terminates **before** the subtraction that
    would cross midnight into the previous calendar day, since any further
    entries would lie outside the race bounds. This replaces the earlier
    heuristic that only inspected the resulting time string and failed when the
    arithmetic wrapped around midnight.
    
    Args:
        rows: Existing table rows (will be modified)
        mean_stint_time: Mean duration of completed stints
        starting_tires_left: Remaining tires after completed stints
        prev_stint_time: Duration of the previous stint
    """
    # Get last pit time from last completed stint
    current_pit_time = rows[-1][ColumnIndex.PIT_END_TIME]
    tires_left = starting_tires_left
    
    while True:
        time_of_day = calculate_time_of_day(prev_time_of_day, prev_stint_time)

        # Determine whether subtracting another mean stint would cross
        # into the previous day. We still want to *add* that final crossing
        # row (it represents the last stint that runs past midnight), but we
        # should stop afterwards to avoid an infinite loop.
        cross = is_last_stint(current_pit_time, mean_stint_time)

        # Calculate next pit time by subtracting mean stint time
        next_pit = _subtract_time_from_pit_time(current_pit_time, mean_stint_time)

        # Determine tire changes for pending stint
        # If last stint had no tire changes, assume full set; otherwise none
        last_tire_change = int(rows[-1][ColumnIndex.TIRES_CHANGED])
        pending_tires_changed = FULL_TIRE_SET if last_tire_change == NO_TIRE_CHANGE else NO_TIRE_CHANGE
        
        # Adjust tires_left
        if pending_tires_changed == FULL_TIRE_SET:
            tires_left -= FULL_TIRE_SET
        
        # determine actual pit time and stint duration
        if cross:
            # final crossing stint: show midnight as the pit end time. the
            # desired duration is the interval from midnight back up to the
            # current pit time (which is earlier than the mean). this is just
            # \`current - midnight\`, not a full 24‑hour wrap.
            pit_display = "00:00:00"
            from datetime import datetime, date, time as _time
            t_cur = datetime.strptime(current_pit_time, "%H:%M:%S").time()
            dt_cur = datetime.combine(date.today(), t_cur)
            dt_mid = datetime.combine(date.today(), _time(0, 0))
            duration = dt_cur - dt_mid
        else:
            pit_display = next_pit
            duration = mean_stint_time

        row = create_table_row(
            stint_type="Single",
            driver="",
            status="Pending",
            pit_time=pit_display,
            tires_changed=pending_tires_changed,
            tires_left=tires_left,
            stint_time=format_timedelta(duration),
            time_of_day=time_of_day
        )
        rows.append(row)

        prev_time_of_day = time_of_day
        prev_stint_time = duration

        # if the subtraction we just performed crossed midnight, we added the
        # final row (with 00:00:00) and should exit the loop.
        if cross:
            break

        # otherwise continue with the new pit as the starting point
        current_pit_time = next_pit


def _subtract_time_from_pit_time(pit_time_str: str, delta: timedelta) -> str:
    """
    Subtract a timedelta from a pit time string.
    
    Args:
        pit_time_str: Time string in format "HH:MM:SS"
        delta: Time duration to subtract
        
    Returns:
        New time string in format "HH:MM:SS"
    """
    pit_time = datetime.strptime(pit_time_str, "%H:%M:%S").time()
    delta_as_time = timedelta_to_time(delta)
    
    # Combine with today's date for arithmetic
    pit_datetime = datetime.combine(datetime.today(), pit_time)
    delta_timedelta = timedelta(
        hours=delta_as_time.hour,
        minutes=delta_as_time.minute,
        seconds=delta_as_time.second
    )
    
    result_datetime = pit_datetime - delta_timedelta
    return result_datetime.time().strftime("%H:%M:%S")


