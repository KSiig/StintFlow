"""
Stint type calculation functions for table model.

Handles recalculating stint types based on tire changes and
redistributing tire changes when stint types are edited.
"""

from PyQt6.QtCore import Qt

from ..TableRoles import TableRoles
from ..stint_helpers import get_stint_type, get_stint_length, get_default_tire_dict
from ..table_constants import ColumnIndex
import copy

# Constants
FULL_TIRE_SET = 4  # Number of tires in a full set change
NO_TIRE_CHANGE = 0  # No tires changed


def recalculate_stint_types(
    data: list[list],
    index_fn,
    row_count_fn,
    emit_editors_refresh,
    emit_data_changed,
    repaint_table
) -> None:
    """
    Recalculate stint types for all rows based on tire changes.
    
    Args:
        data: Table data array (will be modified)
        index_fn: Function to create QModelIndex
        row_count_fn: Function to get row count
        emit_editors_refresh: Function to emit editorsNeedRefresh signal
        emit_data_changed: Function to emit dataChanged signal
        repaint_table: Function to repaint table
    """
    if not data:
        return
    
    start_of_stint = 0
    
    for i, row in enumerate(data):
        tires_changed = int(row[ColumnIndex.TIRES_CHANGED])
        stint_amounts = i - start_of_stint
        
        if tires_changed:
            # Tire change marks end of previous stint and potential start of new one
            stint_type = _calculate_stint_type_with_tire_change(
                data, start_of_stint, i, stint_amounts
            )
            start_of_stint = i + 1
        elif stint_amounts and not tires_changed:
            # Multi-stint in progress - update first row, clear current
            data[start_of_stint][ColumnIndex.STINT_TYPE] = get_stint_type(stint_amounts)
            stint_type = ""
        else:
            stint_type = get_stint_type(stint_amounts)
        
        row[ColumnIndex.STINT_TYPE] = stint_type
    
    # Notify views
    emit_editors_refresh()
    emit_data_changed(
        index_fn(0, 0),
        index_fn(row_count_fn() - 1, ColumnIndex.STINT_TIME),
        [Qt.ItemDataRole.DisplayRole, TableRoles.TiresRole]
    )
    repaint_table()


def _calculate_stint_type_with_tire_change(
    data: list[list],
    start_of_stint: int,
    current_row: int,
    stint_amounts: int
) -> str:
    """
    Calculate stint type when a tire change is present.
    
    Args:
        data: Table data array
        start_of_stint: Index where current stint started
        current_row: Current row being processed
        stint_amounts: Number of rows in current stint
        
    Returns:
        Stint type string ("Single", "", etc.)
    """
    if start_of_stint == current_row:
        # First row of stint has tire change → Single stint
        return "Single"
    else:
        # Multi-stint completed - update start row with correct type
        data[start_of_stint][ColumnIndex.STINT_TYPE] = get_stint_type(stint_amounts)
        return ""  # Clear current row (it's the end of a multi-stint)


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
    
    old_tire_changes = []

    # First loop — copy rows + column values
    for i in range(total_rows):
        if int(data[i][ColumnIndex.TIRES_CHANGED]) > 0:
            old_tire_changes.append({
                "row": i,
                "value": data[i][ColumnIndex.TIRES_CHANGED],
                "tires": copy.deepcopy(tires[i])
            })

    # Clear all tire changes
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
    
    # Force tire change at end of edited stint
    forced_row = min(row + new_len - 1, total_rows - 1)
    data[forced_row][ColumnIndex.TIRES_CHANGED] = str(FULL_TIRE_SET)
    tires[forced_row] = get_default_tire_dict(True)
    
    # Recalculate remaining tires
    recalc_tires_left_fn()
