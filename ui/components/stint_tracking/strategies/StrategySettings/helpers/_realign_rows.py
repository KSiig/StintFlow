from __future__ import annotations

from datetime import datetime, timedelta

from ui.models.stint_helpers import calculate_time_of_day, get_default_tire_dict
from ui.models.table_constants import FULL_TIRE_SET
from ui.models.table_processors.stint_processor import _subtract_time_from_pit_time, is_last_stint


def _realign_rows(self, new_mean_sec: int) -> None:
    """Adjust pending rows to align with a new mean stint time."""
    model_data = self.strategy.setdefault('model_data', {})
    rows: list[dict] = model_data.setdefault('rows', [])

    if not rows:
        return

    completed_count = 0
    for i, row in enumerate(rows):
        if row.get('status'):
            completed_count = i + 1
        else:
            break

    if completed_count == 0:
        return

    last_completed = rows[completed_count - 1]
    base_prev_tod = timedelta(seconds=int(last_completed.get('time_of_day_seconds', 0)))
    base_prev_stint = timedelta(seconds=int(last_completed.get('stint_time_seconds', 0)))

    for i in range(completed_count, len(rows)):
        rows[i]['stint_time_seconds'] = new_mean_sec

    current_pit = last_completed.get('pit_end_time', '00:00:00')
    mean_td = timedelta(seconds=new_mean_sec)

    keep_len = len(rows)
    for i in range(completed_count, len(rows)):
        if is_last_stint(current_pit, mean_td):
            rows[i]['pit_end_time'] = "00:00:00"
            keep_len = i + 1
            break

        current_pit = _subtract_time_from_pit_time(current_pit, mean_td)
        rows[i]['pit_end_time'] = current_pit

    if keep_len < len(rows):
        rows[:] = rows[:keep_len]
        model_data['tires'] = model_data.get('tires', [])[:keep_len]

    if len(rows) > completed_count:
        current_pit = rows[-1]['pit_end_time']
    else:
        current_pit = last_completed.get('pit_end_time', '00:00:00')

    pending_count = len(rows) - completed_count
    next_change = 0 if pending_count % 2 == 0 else 4

    try:
        tires_left = int(rows[-1]['tires_left'])
    except Exception:
        tires_left = 0

    while True:
        if current_pit == "00:00:00":
            break

        crossed = is_last_stint(current_pit, mean_td)
        next_pit = _subtract_time_from_pit_time(current_pit, mean_td)

        if crossed:
            pit_display = "00:00:00"
            t_cur = datetime.strptime(current_pit, "%H:%M:%S").time()
            duration_sec = int(
                (
                    datetime.combine(datetime.today(), t_cur)
                    - datetime.combine(datetime.today(), datetime.min.time())
                ).total_seconds()
            )
        else:
            pit_display = next_pit
            duration_sec = new_mean_sec

        if next_change == 4:
            tires_left -= FULL_TIRE_SET

        rows.append(
            {
                "stint_type": "Single",
                "name": "",
                "status": False,
                "pit_end_time": pit_display,
                "tires_changed": next_change,
                "tires_left": tires_left,
                "stint_time_seconds": duration_sec,
                "time_of_day_seconds": 0,
            }
        )
        model_data.setdefault('tires', []).append(
            get_default_tire_dict(next_change == 4)
        )

        if crossed:
            break

        current_pit = next_pit
        next_change = 4 if next_change == 0 else 0

    prev_tod_str = _timedelta_to_hms(base_prev_tod)
    prev_stint_td = base_prev_stint

    for i in range(completed_count, len(rows)):
        new_tod = calculate_time_of_day(prev_tod_str, prev_stint_td)
        h, m, s = [int(x) for x in new_tod.split(":")]
        rows[i]['time_of_day_seconds'] = h * 3600 + m * 60 + s
        prev_tod_str = new_tod
        prev_stint_td = timedelta(seconds=int(rows[i].get('stint_time_seconds', 0)))


def _timedelta_to_hms(td: timedelta) -> str:
    total = int(td.total_seconds())
    h = total // 3600
    m = (total % 3600) // 60
    s = total % 60
    return f"{h:02d}:{m:02d}:{s:02d}"
