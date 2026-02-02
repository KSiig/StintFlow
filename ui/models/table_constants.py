"""
Constants and type definitions for table model.

Defines column indices, type aliases, and other constants used throughout
the table model and related processors.
"""

from typing import TypeAlias


# Type aliases for complex types
TableRow: TypeAlias = list[str]
TireData: TypeAlias = dict[str, dict | bool]


class ColumnIndex:
    """Column indices for table data."""
    STINT_TYPE = 0
    DRIVER = 1
    STATUS = 2
    PIT_END_TIME = 3
    TIRES_CHANGED = 4
    TIRES_LEFT = 5
    STINT_TIME = 6
