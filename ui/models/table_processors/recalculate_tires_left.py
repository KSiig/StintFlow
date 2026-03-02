"""Recalculate remaining tires for each row."""

from core.database import get_event
from core.errors import log

from ..table_constants import ColumnIndex
from .count_tire_changes import count_tire_changes


def recalculate_tires_left(
    data: list[list],
    tires: list[dict],
    event_id: str,
    recalc_stint_types_fn,
) -> None:
    """Update remaining tires per row and trigger stint-type recalculation."""
    event = get_event(event_id)
    if not event:
        log(
            "WARNING",
            "Cannot recalculate tires - event not found",
            category="table_model",
            action="recalc_tires",
        )
        return

    tires_left = int(event.get("tires", 0))

    for i, row in enumerate(data):
        if i < len(tires):
            _, medium_changed = count_tire_changes(tires[i])
            tires_left -= medium_changed

        row[ColumnIndex.TIRES_LEFT] = str(tires_left)

    recalc_stint_types_fn()
