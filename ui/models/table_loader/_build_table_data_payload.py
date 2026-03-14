"""Build the shared table-data payload from database records."""

from __future__ import annotations

from collections.abc import Callable
from datetime import timedelta
from typing import Any

from core.database import get_event, get_session, get_stints
from core.errors import log
from ui.models.TableModel.constants import (
    DEFAULT_RACE_LENGTH,
    DEFAULT_START_TIME,
    DEFAULT_TIRE_COUNT,
)
from ui.models.stint_helpers import get_default_tire_dict
from ui.models.table_constants import NO_TIRE_CHANGE
from ui.models.table_processors import convert_stints_to_table, count_tire_changes

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ui.models.SelectionModel import SelectionModel


def _build_table_data_payload(
    selection_model: SelectionModel,
    pit_time_parser: Callable[[dict[str, Any]], Any] | None = None,
) -> dict[str, Any] | None:
    """Load event + stint data and return a normalized table payload."""
    if not selection_model.event_id or not selection_model.session_id:
        log(
            "WARNING",
            "No event or session selected - cannot load table data",
            category="table_model",
            action="load_data",
        )
        return None

    session = get_session(selection_model.session_id)
    event = get_event(selection_model.event_id)
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
            f"Event {selection_model.event_id} not found - using defaults",
            category="table_model",
            action="load_data",
        )

    if session and session.get("tires_remaining_at_green_flag") is not None:
        total_tires = str(session.get("tires_remaining_at_green_flag"))

    stints = get_stints(selection_model.session_id)
    if pit_time_parser is None:
        stints = sorted(stints, key=lambda stint: stint.get("pit_end_time", None) or 0, reverse=True)
    else:
        stints = sorted(stints, key=pit_time_parser, reverse=True)

    tires = [stint.get("tire_data", {}) for stint in stints]

    rows, mean_stint_time, last_tire_change = convert_stints_to_table(
        stints,
        total_tires,
        race_length,
        count_tire_changes,
        start_time,
    )

    index = 0 if last_tire_change is NO_TIRE_CHANGE else 1
    while len(tires) < len(rows):
        # Alternate tire-change status for generated rows; invert because
        # get_default_tire_dict expects whether tires were changed on entry
        tires_changed = bool(index % 2)
        tires.append(get_default_tire_dict(not tires_changed))
        index += 1

    return {
        "mean_stint_time": mean_stint_time if mean_stint_time is not None else timedelta(0),
        "rows": rows,
        "stints": stints,
        "tires": tires,
        "total_tires": total_tires,
    }