from ui.models.table_constants import ColumnIndex, TableRow


def is_completed_row(data: list[TableRow], row: int) -> bool:
    """Return True if the given row represents a completed stint."""
    if row >= len(data):
        return False
    status = data[row][ColumnIndex.STATUS]
    return "Completed" in str(status)
