"""Generate pending stints based on mean stint time."""

from datetime import date, datetime, time as time_type, timedelta

from ..stint_helpers import calculate_time_of_day, format_timedelta, is_last_stint
from ..table_constants import ColumnIndex, FULL_TIRE_SET, NO_TIRE_CHANGE, TableRow
from ..table_utils import create_table_row
from ._subtract_time_from_pit_time import _subtract_time_from_pit_time


def generate_pending_stints(
    rows: list[TableRow],
    mean_stint_time: timedelta,
    starting_tires_left: int,
    prev_time_of_day: str,
    prev_stint_time: timedelta,
) -> None:
    """Append pending stints until the race crosses midnight."""
    if not rows:
        return

    current_pit_time = rows[-1][ColumnIndex.PIT_END_TIME]
    tires_left = starting_tires_left

    while True:
        time_of_day = calculate_time_of_day(prev_time_of_day, prev_stint_time)
        cross = is_last_stint(current_pit_time, mean_stint_time)

        next_pit = _subtract_time_from_pit_time(current_pit_time, mean_stint_time)

        last_tire_change = int(rows[-1][ColumnIndex.TIRES_CHANGED])
        pending_tires_changed = FULL_TIRE_SET if last_tire_change == NO_TIRE_CHANGE else NO_TIRE_CHANGE

        if pending_tires_changed == FULL_TIRE_SET:
            tires_left -= FULL_TIRE_SET

        if cross:
            pit_display = "00:00:00"
            t_cur = datetime.strptime(current_pit_time, "%H:%M:%S").time()
            dt_cur = datetime.combine(date.today(), t_cur)
            dt_mid = datetime.combine(date.today(), time_type(0, 0))
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
            time_of_day=time_of_day,
        )
        rows.append(row)

        prev_time_of_day = time_of_day
        prev_stint_time = duration

        if cross:
            break

        current_pit_time = next_pit
