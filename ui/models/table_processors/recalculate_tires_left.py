"""Recalculate remaining tires for each row."""

from core.errors import log

from ..table_constants import ColumnIndex
from .count_tire_changes import count_tire_changes


def recalculate_tires_left(
    data: list[list],
    tires: list[dict],
    total_tires: int,
    recalc_stint_types_fn,
) -> None:
    """Update remaining tires per row and trigger stint-type recalculation."""
    if total_tires is None:
        log(
            "WARNING",
            "Cannot recalculate tires - total tire count unavailable",
            category="table_model",
            action="recalc_tires",
        )
        return

    tires_left = int(total_tires)

    for i, row in enumerate(data):
        if i < len(tires):
            _, medium_changed = count_tire_changes(tires[i])
            tires_left -= medium_changed

        row[ColumnIndex.TIRES_LEFT] = str(tires_left)

    recalc_stint_types_fn()
