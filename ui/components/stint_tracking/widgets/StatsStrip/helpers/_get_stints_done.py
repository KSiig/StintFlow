"""Get number of included completed stints from the table model context."""

from __future__ import annotations

from core.errors import log
from ui.models.table_constants import ColumnIndex


def _get_stints_done(context: dict = None) -> tuple[str, int]:
    """Return included completed stints as ratio and completion percentage.

    Expected context shape:
        {"table_model": <TableModel instance>}
    """
    context_data = context or {}
    table_model = context_data.get("table_model")

    if table_model is None:
        log(
            'DEBUG',
            'TableModel missing in stats context; returning stints done as 0/0',
            category='stats_strip',
            action='get_stints_done',
        )
        return "0/0", "0%"

    rows = getattr(table_model, '_data', []) or []

    completed_included = 0
    total_included = 0
    for row in rows:
        try:
            # ensure the expected index exists before counting the row
            status = str(row[ColumnIndex.STATUS])
            total_included += 1

            # normalize and check for completed status (match other helper)
            if status.strip().lower() != 'completed':
                continue

            completed_included += 1
        except Exception:
            # malformed row or missing columns; skip entirely
            continue

    percent_done = int((completed_included / total_included) * 100) if total_included > 0 else 0
    done_ratio = f"{completed_included}/{total_included}"
    return done_ratio, f"{percent_done}%"
