"""
Utility functions for table model operations.

Helper functions for creating rows, checking row status, and other
common operations used by the table model.
"""

from .table_constants import TableRow, ColumnIndex


def create_table_row(
    stint_type: str,
    driver: str,
    status: str,
    pit_time: str,
    tires_changed: int,
    tires_left: int,
    stint_time: str
) -> TableRow:
    """
    Create a standardized table row.
    
    Args:
        stint_type: Stint type (Single, Double, etc.)
        driver: Driver name
        status: Status text (Completed ✅, Pending ⏳)
        pit_time: Pit end time in HH:MM:SS format
        tires_changed: Number of tires changed
        tires_left: Remaining tires
        stint_time: Stint duration as formatted string
        
    Returns:
        Standardized table row as list of strings
    """
    return [
        stint_type,
        driver,
        status,
        pit_time,
        str(tires_changed),
        str(tires_left),
        stint_time
    ]


def is_completed_row(data: list[TableRow], row: int) -> bool:
    """
    Check if row represents a completed stint.
    
    Args:
        data: Table data array
        row: Row index to check
        
    Returns:
        True if row is completed, False otherwise
    """
    if row >= len(data):
        return False
    status = data[row][ColumnIndex.STATUS]
    return "Completed" in str(status)
