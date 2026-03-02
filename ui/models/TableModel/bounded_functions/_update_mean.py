from datetime import timedelta

from core.database import get_event
from core.errors import log
from ui.models.table_constants import ColumnIndex, NO_TIRE_CHANGE
from ui.models.table_processors import generate_pending_stints
from ui.models.stint_helpers import calc_mean_stint_time, calculate_stint_time, get_default_tire_dict

from ..constants import DEFAULT_RACE_LENGTH


def update_mean(self, update_pending: bool = True) -> None:
    """Recalculate mean stint time and regenerate pending rows if needed."""
    if not self.selection_model.session_id:
        return

    self.beginResetModel()
    try:
        event = get_event(self.selection_model.event_id)
        race_length = event.get("length", DEFAULT_RACE_LENGTH) if event else DEFAULT_RACE_LENGTH

        completed_count = 0
        for i, row in enumerate(self._data):
            if "Completed" in str(row[ColumnIndex.STATUS]):
                completed_count = i + 1
            else:
                break

        if completed_count == 0:
            self._mean_stint_time = timedelta(0)
            return

        stint_times: list[timedelta] = []
        for i in range(completed_count):
            stint_time_str = str(self._data[i][ColumnIndex.STINT_TIME])
            stint_duration = None
            try:
                h, m, s = map(int, stint_time_str.split(":"))
                stint_duration = timedelta(hours=h, minutes=m, seconds=s)
            except Exception:
                try:
                    prev_pit = race_length if i == 0 else str(self._data[i - 1][ColumnIndex.PIT_END_TIME])
                    pit_time = str(self._data[i][ColumnIndex.PIT_END_TIME])
                    stint_duration = calculate_stint_time(prev_pit, pit_time)
                except Exception:
                    stint_duration = timedelta(0)

            meta = self._meta[i] if i < len(self._meta) else None
            if not (isinstance(meta, dict) and meta.get("excluded", False)):
                stint_times.append(stint_duration)

        self._mean_stint_time = calc_mean_stint_time(stint_times)

        if getattr(self, "_is_strategy", False):
            self._repaint_table()
            return

        last_completed = self._data[completed_count - 1]
        try:
            tires_left = int(last_completed[ColumnIndex.TIRES_LEFT])
        except Exception:
            tires_left = 0

        self._data = self._data[:completed_count]
        self._tires = self._tires[:completed_count]

        if update_pending:
            generate_pending_stints(self._data, self._mean_stint_time, tires_left)
            last_tire_change = last_completed[ColumnIndex.TIRES_CHANGED]
            i = 0 if last_tire_change is NO_TIRE_CHANGE else 1
            while len(self._tires) < len(self._data):
                tires_changed = bool(i % 2)
                self._tires.append(get_default_tire_dict(not tires_changed))
                i += 1
            self._recalculate_stint_types()

        self._repaint_table()

    except Exception as exc:  # pragma: no cover - defensive logging
        log("ERROR", f"Failed to update mean/pending rows: {exc}", category="table_model", action="update_mean")
    finally:
        self.endResetModel()
