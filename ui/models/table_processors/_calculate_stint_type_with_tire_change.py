"""Helper to determine stint type when a tire change occurs."""

from ..stint_helpers import get_stint_type
from ..table_constants import ColumnIndex


def _calculate_stint_type_with_tire_change(
    data: list[list],
    start_of_stint: int,
    current_row: int,
    stint_amounts: int,
) -> str:
    """Return the correct stint type string when a tire change is present."""
    if start_of_stint == current_row:
        return "Single"

    data[start_of_stint][ColumnIndex.STINT_TYPE] = get_stint_type(stint_amounts)
    return ""
