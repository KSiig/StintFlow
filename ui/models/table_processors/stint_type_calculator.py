"""
Stint type calculation functions for table model.

Handles recalculating stint types based on tire changes and
redistributing tire changes when stint types are edited.
"""

from PyQt6.QtCore import Qt

from ..TableRoles import TableRoles
from ..stint_helpers import get_stint_type, get_stint_length, get_default_tire_dict
from ..table_constants import ColumnIndex


def recalculate_stint_types(
    data: list[list],
    index_fn,
    row_count_fn,
    emit_editors_refresh_fn,
    emit_data_changed_fn,
    repaint_table_fn
) -> None:
    """
    Recalculate stint types for all rows based on tire changes.
    
    Args:
        data: Table data array (will be modified)
        index_fn: Function to create QModelIndex
        row_count_fn: Function to get row count
        emit_editors_refresh_fn: Function to emit editorsNeedRefresh signal
        emit_data_changed_fn: Function to emit dataChanged signal
        repaint_table_fn: Function to repaint table
    """
    if not data:
        return
    
    start_of_stint = 0
    
    for i, row in enumerate(data):
        tires_changed = int(row[ColumnIndex.TIRES_CHANGED])
        stint_amounts = i - start_of_stint
        stint_type = get_stint_type(stint_amounts)
        
        if tires_changed:
            stint_type = "Single" if start_of_stint == i else ""
            start_of_stint = i + 1
        elif stint_amounts and not tires_changed:
            # Multi-stint - update start row, clear current
            data[start_of_stint][ColumnIndex.STINT_TYPE] = get_stint_type(stint_amounts)
            stint_type = ""
        
        row[ColumnIndex.STINT_TYPE] = stint_type
    
    # Notify views
    emit_editors_refresh_fn()
    emit_data_changed_fn(
        index_fn(0, 0),
        index_fn(row_count_fn() - 1, ColumnIndex.STINT_TIME),
        [Qt.ItemDataRole.DisplayRole, TableRoles.TiresRole]
    )
    repaint_table_fn()


def recalculate_tires_changed(
    data: list[list],
    tires: list[dict],
    row: int,
    old_value: str,
    total_rows: int,
    recalc_tires_left_fn
) -> None:
    """
    Recalculate tire changes after stint type edit.
    
    When a stint type changes (e.g., Single → Double), tire changes
    need to be redistributed to the new end of the stint.
    
    Args:
        data: Table data array (will be modified)
        tires: Tire metadata array (will be modified)
        row: Row index of edited cell
        old_value: Previous stint type value
        total_rows: Total number of rows
        recalc_tires_left_fn: Function to recalculate remaining tires
    """
    if row >= total_rows:
        return
    
    old_len = get_stint_length(old_value)
    new_len = get_stint_length(data[row][ColumnIndex.STINT_TYPE])
    delta = new_len - old_len
    
    # Snapshot current tire changes
    old_tire_changes = [
        {"row": i, "value": data[i][ColumnIndex.TIRES_CHANGED], "tires": tires[i]}
        for i in range(total_rows) if int(data[i][ColumnIndex.TIRES_CHANGED]) > 0
    ]
    
    # Clear all tire changes
    for r in range(total_rows):
        data[r][ColumnIndex.TIRES_CHANGED] = "0"
        tires[r] = get_default_tire_dict(False)
    
    # Re-apply tire changes with adjusted positions
    for tc in old_tire_changes:
        old_row = tc["row"]
        
        if row <= old_row < row + old_len:
            # Tire change was in edited stint → move to new end
            new_row = min(row + new_len - 1, total_rows - 1)
        elif old_row >= row + old_len:
            # Downstream tire change → shift by delta
            new_row = old_row + delta
        else:
            # Upstream → no change
            new_row = old_row
        
        # Apply if within bounds
        if 0 <= new_row < total_rows:
            data[new_row][ColumnIndex.TIRES_CHANGED] = tc["value"]
            tires[new_row] = tc["tires"]
    
    # Force tire change at end of edited stint
    forced_row = min(row + new_len - 1, total_rows - 1)
    data[forced_row][ColumnIndex.TIRES_CHANGED] = "4"
    tires[forced_row] = get_default_tire_dict(True)
    
    # Recalculate remaining tires
    recalc_tires_left_fn()
