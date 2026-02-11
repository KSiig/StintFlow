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
    format_timedelta,
    calc_mean_stint_time,
    timedelta_to_time,
    is_last_stint
)

# Constants
FULL_TIRE_SET = 4  # Number of tires in a full set change
NO_TIRE_CHANGE = 0  # No tires changed


def convert_stints_to_table(
    stints: list[dict],
    starting_tires: str,
    starting_time: str,
    count_tire_changes_fn
) -> tuple[list[TableRow], timedelta]:
    """
    Convert stint documents to table row format.
    
    Args:
        stints: List of stint documents from database
        starting_tires: Total tire count at race start
        starting_time: Race start time
        count_tire_changes_fn: Function to count tire changes
        
    Returns:
        List of rows with completed and pending stints
    """
    if not stints:
        return [], timedelta(0)
    
    # Process completed stints
    rows, tires_left, stint_times = process_completed_stints(
        stints, starting_tires, starting_time, count_tire_changes_fn
    )
    
    # Generate pending stints
    if stint_times:
        generate_pending_stints(rows, stint_times, tires_left)
    
    return rows, calc_mean_stint_time(stint_times)


def process_completed_stints(
    stints: list[dict],
    starting_tires: str,
    starting_time: str,
    count_tire_changes_fn
) -> tuple[list[TableRow], int, list[timedelta]]:
    """
    Process completed stints into table rows.
    
    Args:
        stints: List of stint documents
        starting_tires: Total tire count at start
        starting_time: Race start time
        count_tire_changes_fn: Function to count tire changes
        
    Returns:
        Tuple of (rows, remaining_tires, stint_times)
    """
    rows = []
    stint_times = []
    prev_pit_time = starting_time
    tires_left = int(starting_tires)
    start_of_stint = 0
    
    for i, stint in enumerate(stints):
        # Calculate stint duration
        stint_time = calculate_stint_time(prev_pit_time, stint.get('pit_end_time', '00:00:00'))
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
            stint_time=format_timedelta(stint_time)
        )
        rows.append(row)
        
        prev_pit_time = stint.get('pit_end_time', '00:00:00')
    
    return rows, tires_left, stint_times


def generate_pending_stints(
    rows: list[TableRow],
    stint_times: list[timedelta],
    starting_tires_left: int
) -> None:
    """
    Generate pending stints based on mean stint time.
    
    Args:
        rows: Existing table rows (will be modified)
        stint_times: List of completed stint durations
        starting_tires_left: Remaining tires after completed stints
    """
    mean_stint_time = calc_mean_stint_time(stint_times)
    
    # Get last pit time from last completed stint
    current_pit_time = rows[-1][ColumnIndex.PIT_END_TIME]
    tires_left = starting_tires_left
    
    while True:
        # Calculate next pit time by subtracting mean stint time
        current_pit_time = _subtract_time_from_pit_time(current_pit_time, mean_stint_time)
        
        # Determine tire changes for pending stint
        # If last stint had no tire changes, assume full set; otherwise none
        last_tire_change = int(rows[-1][ColumnIndex.TIRES_CHANGED])
        pending_tires_changed = FULL_TIRE_SET if last_tire_change == NO_TIRE_CHANGE else NO_TIRE_CHANGE
        
        # Adjust tires_left
        if pending_tires_changed == FULL_TIRE_SET:
            tires_left -= FULL_TIRE_SET
        
        # Add pending row
        row = create_table_row(
            stint_type="Single",
            driver="",
            status="Pending",
            pit_time=current_pit_time,
            tires_changed=pending_tires_changed,
            tires_left=tires_left,
            stint_time=format_timedelta(mean_stint_time)
        )
        rows.append(row)
        
        # Check if this is the last stint before race end
        if is_last_stint(current_pit_time, timedelta_to_time(mean_stint_time)):
            break


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


