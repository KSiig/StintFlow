"""Recalculate stint types across the table."""

from PyQt6.QtCore import Qt

from ..TableRoles import TableRoles
from ..stint_helpers import get_stint_type
from ..table_constants import ColumnIndex
from ._calculate_stint_type_with_tire_change import _calculate_stint_type_with_tire_change


def recalculate_stint_types(
    data: list[list],
    index_fn,
    row_count_fn,
    emit_editors_refresh,
    emit_data_changed,
    repaint_table,
) -> None:
    """Refresh stint types in response to tire-change edits."""
    if not data:
        return

    start_of_stint = 0

    for i, row in enumerate(data):
        tires_changed = int(row[ColumnIndex.TIRES_CHANGED])
        stint_amounts = i - start_of_stint

        if tires_changed:
            stint_type = _calculate_stint_type_with_tire_change(data, start_of_stint, i, stint_amounts)
            start_of_stint = i + 1
        elif stint_amounts and not tires_changed:
            data[start_of_stint][ColumnIndex.STINT_TYPE] = get_stint_type(stint_amounts)
            stint_type = ""
        else:
            stint_type = get_stint_type(stint_amounts)

        row[ColumnIndex.STINT_TYPE] = stint_type

    emit_editors_refresh()
    emit_data_changed(
        index_fn(0, 0),
        index_fn(row_count_fn() - 1, ColumnIndex.STINT_TIME),
        [Qt.ItemDataRole.DisplayRole, TableRoles.TiresRole],
    )
    repaint_table()
