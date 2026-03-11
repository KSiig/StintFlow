"""Load table data from the database and initialize model state."""

from core.database import get_event, get_stints
from core.errors import log
from ui.models.table_constants import NO_TIRE_CHANGE
from ui.models.table_processors import convert_stints_to_table, count_tire_changes
from ui.models.stint_helpers import get_default_tire_dict

from ..constants import DEFAULT_RACE_LENGTH, DEFAULT_START_TIME, DEFAULT_TIRE_COUNT


def _load_data_from_database(self) -> None:
    """Load stint data from database and convert to table format."""
    if not self.selection_model.event_id or not self.selection_model.session_id:
        log("WARNING", "No event or session selected - cannot load data", category="table_model", action="load_data")
        return

    log(
        "DEBUG",
        f"Loading data for event {self.selection_model.event_id}, session {self.selection_model.session_id}",
        category="table_model",
        action="load_data",
    )

    event = get_event(self.selection_model.event_id)
    if event:
        total_tires = str(event.get("tires", DEFAULT_TIRE_COUNT))
        race_length = event.get("length", DEFAULT_RACE_LENGTH)
        start_time = event.get("start_time", DEFAULT_START_TIME)
    else:
        total_tires = DEFAULT_TIRE_COUNT
        race_length = DEFAULT_RACE_LENGTH
        start_time = DEFAULT_START_TIME
        log(
            "WARNING",
            f"Event {self.selection_model.event_id} not found - using defaults",
            category="table_model",
            action="load_data",
        )

    try:
        self._event_tire_count = int(total_tires)
    except Exception:
        self._event_tire_count = int(DEFAULT_TIRE_COUNT)

    stints = get_stints(self.selection_model.session_id)
    stints = sorted(stints, key=self._parse_pit_time, reverse=True)

    self._tires = [stint.get("tire_data", {}) for stint in stints]
    self._meta = [
        {"id": str(stint.get("_id")), "excluded": bool(stint.get("excluded", False))}
        for stint in stints
    ]

    rows, mean_stint_time, last_tire_change = convert_stints_to_table(
        stints,
        total_tires,
        race_length,
        count_tire_changes,
        start_time,
    )
    self._data = rows
    self._mean_stint_time = mean_stint_time

    i = 0 if last_tire_change is NO_TIRE_CHANGE else 1
    while len(self._tires) < len(self._data):
        tires_changed = bool(i % 2)
        self._tires.append(get_default_tire_dict(not tires_changed))
        i += 1

    self._recalculate_stint_types()
    self._repaint_table()
