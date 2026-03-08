"""Get tires left from the latest included completed stint."""

from __future__ import annotations

from core.errors import log
from ui.models.table_constants import ColumnIndex


def _get_tires_left(context: dict = None) -> int:
    """Return tires left from the first included completed row.

    Expected context shape:
        {"table_model": <TableModel instance>}
    """
    context_data = context or {}
    table_model = context_data.get("table_model")

    if table_model is None:
        log(
            'DEBUG',
            'TableModel missing in stats context; returning tires left as 0',
            category='stats_strip',
            action='get_tires_left',
        )
        return 0

    rows = getattr(table_model, '_data', []) or []

    tires_left = 0

    for row in rows:
        try:
            status = str(row[ColumnIndex.STATUS])

            if 'Completed' not in status:
                return tires_left

            tires_left = int(str(row[ColumnIndex.TIRES_LEFT]))

        except Exception:
            continue

    return 0
