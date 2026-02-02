"""
Stint processor for converting database stints to table rows.

Handles processing of completed stints and generation of pending stints
based on mean stint times.
"""

from datetime import datetime, date, timedelta

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


def convert_stints_to_table(
    stints: list[dict],
    starting_tires: str,
    starting_time: str,
    count_tire_changes_fn
) -> list[TableRow]:
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
        return []
    
    # Process completed stints
    rows, tires_left, stint_times = process_completed_stints(
        stints, starting_tires, starting_time, count_tire_changes_fn
    )
    
    # Generate pending stints
    if stint_times:
        generate_pending_stints(rows, stint_times, tires_left)
    
    return rows


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
            status="Completed ✅",
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
    break_next = False
    
    while True:
        # Calculate next pit time by subtracting mean stint time
        t1 = datetime.strptime(current_pit_time, "%H:%M:%S").time()
        t2 = timedelta_to_time(mean_stint_time)
        
        dt = datetime.combine(datetime.today(), t1)
        delta = timedelta(hours=t2.hour, minutes=t2.minute, seconds=t2.second)
        dt_minus = dt - delta
        
        current_pit_time = dt_minus.time().strftime("%H:%M:%S")
        
        # Determine tire changes for pending stint
        # If last stint had no tire changes, assume 4 tires; otherwise 0
        last_tire_change = int(rows[-1][ColumnIndex.TIRES_CHANGED])
        pending_tires_changed = 4 if last_tire_change == 0 else 0
        
        # Adjust tires_left
        if pending_tires_changed == 4:
            tires_left -= 4
        
        # Add pending row
        row = create_table_row(
            stint_type="Single",
            driver="",
            status="Pending ⏳",
            pit_time=current_pit_time,
            tires_changed=pending_tires_changed,
            tires_left=tires_left,
            stint_time=format_timedelta(mean_stint_time)
        )
        rows.append(row)
        
        # Break exactly ONE iteration AFTER this becomes true
        if break_next:
            break
        
        # Check if we've reached the race end
        if is_last_stint(current_pit_time, timedelta_to_time(mean_stint_time)):
            break_next = True
