"""Redistribute tire changes after a stint-type edit."""

import copy

from ..stint_helpers import get_default_tire_dict, get_stint_length
from ..table_constants import ColumnIndex, FULL_TIRE_SET, NO_TIRE_CHANGE


def recalculate_tires_changed(
    data: list[list],
    tires: list[dict],
    row: int,
    old_value: str,
    total_rows: int,
    recalc_tires_left_fn,
) -> None:
    """Reassign tire-change rows to match the new stint type."""
    if row >= total_rows:
        return

    old_len = get_stint_length(old_value)
    new_len = get_stint_length(data[row][ColumnIndex.STINT_TYPE])
    delta = new_len - old_len

    old_tire_changes = []

    for i in range(total_rows):
        if int(data[i][ColumnIndex.TIRES_CHANGED]) > 0:
            old_tire_changes.append(
                {
                    "row": i,
                    "value": data[i][ColumnIndex.TIRES_CHANGED],
                    "tires": copy.deepcopy(tires[i]),
                }
            )

    for r in range(total_rows):
        data[r][ColumnIndex.TIRES_CHANGED] = str(NO_TIRE_CHANGE)
        tires[r] = get_default_tire_dict(False)

    new_tire_positions = {}

    for record in old_tire_changes:
        old_row = record["row"]

        if row <= old_row < row + old_len:
            new_row = min(row + new_len - 1, total_rows - 1)
        elif old_row >= row + old_len:
            new_row = old_row + delta
        else:
            new_row = old_row

        if 0 <= new_row < total_rows:
            new_tire_positions[new_row] = record

    for new_row, record in new_tire_positions.items():
        data[new_row][ColumnIndex.TIRES_CHANGED] = record["value"]
        tires[new_row] = record["tires"]

    forced_row = min(row + new_len - 1, total_rows - 1)
    data[forced_row][ColumnIndex.TIRES_CHANGED] = str(FULL_TIRE_SET)
    tires[forced_row] = get_default_tire_dict(True)

    recalc_tires_left_fn()
