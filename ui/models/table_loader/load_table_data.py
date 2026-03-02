from datetime import timedelta
from typing import Tuple

from core.database import get_event, get_stints
from core.errors import log
from ui.models.table_constants import NO_TIRE_CHANGE
from ui.models.table_processors import convert_stints_to_table, count_tire_changes
from ui.models.stint_helpers import get_default_tire_dict

DEFAULT_TIRE_COUNT = "0"
DEFAULT_RACE_LENGTH = "00:00:00"
DEFAULT_START_TIME = "00:00:00"


def load_table_data(selection_model) -> Tuple[list, list, timedelta]:
    """Load stint data for the given selection."""
    if not selection_model.event_id or not selection_model.session_id:
        log("WARNING", "No event or session selected - cannot load table data", category="table_model", action="load_data")
        return [], [], timedelta(0)

    event = get_event(selection_model.event_id)
    if event:
        total_tires = str(event.get("tires", DEFAULT_TIRE_COUNT))
        race_length = event.get("length", DEFAULT_RACE_LENGTH)
        start_time = event.get("start_time", DEFAULT_START_TIME)
    else:
        total_tires = DEFAULT_TIRE_COUNT
        race_length = DEFAULT_RACE_LENGTH
        start_time = DEFAULT_START_TIME
        log("WARNING", f"Event {selection_model.event_id} not found - using defaults", category="table_model", action="load_data")

    stints = get_stints(selection_model.session_id)
    stints = sorted(stints, key=lambda s: s.get("pit_time", None) or 0, reverse=True)

    tires = [stint.get("tire_data", {}) for stint in stints]

    rows, mean_stint_time, last_tire_change = convert_stints_to_table(
        stints, total_tires, race_length, count_tire_changes, start_time
    )

    i = 0 if last_tire_change is NO_TIRE_CHANGE else 1
    while len(tires) < len(rows):
        tires_changed = bool(i % 2)
        tires.append(get_default_tire_dict(not tires_changed))
        i += 1

    return rows, tires, mean_stint_time
