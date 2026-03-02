"""Constants and type definitions for table model."""

from typing import TypeAlias

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
    TIME_OF_DAY = 7
    ACTIONS = 8


FULL_TIRE_SET = 4
NO_TIRE_CHANGE = 0
