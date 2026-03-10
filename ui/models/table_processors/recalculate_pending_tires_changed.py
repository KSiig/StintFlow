"""Recalculate pending tire-change rows while preserving completed rows."""

from __future__ import annotations

import copy

from ..stint_helpers import get_default_tire_dict, get_stint_length
from ..table_constants import ColumnIndex, FULL_TIRE_SET, NO_TIRE_CHANGE


def recalculate_pending_tires_changed(
    data: list[list],
    tires: list[dict],
    completed_count: int,
) -> None:
    """Reassign pending tire changes without modifying completed rows."""
    total_rows = len(data)
    if total_rows == 0:
        return

    completed_count = max(0, min(completed_count, total_rows))
    if completed_count >= total_rows:
        return

    while len(tires) < total_rows:
        tires.append(get_default_tire_dict(False))

    pending_tire_changes: list[dict] = []

    for row_index in range(completed_count, total_rows):
        if int(data[row_index][ColumnIndex.TIRES_CHANGED]) > 0:
            pending_tire_changes.append(
                {
                    "value": str(data[row_index][ColumnIndex.TIRES_CHANGED]),
                    "tires": copy.deepcopy(tires[row_index]),
                }
            )

        data[row_index][ColumnIndex.TIRES_CHANGED] = str(NO_TIRE_CHANGE)
        tires[row_index] = get_default_tire_dict(False)

    pending_change_index = 0
    row_index = completed_count

    while row_index < total_rows:
        stint_length = max(1, get_stint_length(str(data[row_index][ColumnIndex.STINT_TYPE])))
        tire_change_row = min(row_index + stint_length - 1, total_rows - 1)

        if pending_change_index < len(pending_tire_changes):
            record = pending_tire_changes[pending_change_index]
            data[tire_change_row][ColumnIndex.TIRES_CHANGED] = str(record["value"])
            tires[tire_change_row] = record["tires"]
            pending_change_index += 1
        else:
            data[tire_change_row][ColumnIndex.TIRES_CHANGED] = str(FULL_TIRE_SET)
            tires[tire_change_row] = get_default_tire_dict(True)

        row_index = tire_change_row + 1