"""Get longest completed stint time from the table model context."""

from __future__ import annotations

from datetime import timedelta

from core.errors import log
from core.utilities import format_stint_time
from ui.models.table_constants import ColumnIndex


def _parse_stint_time(value) -> timedelta:
    """Convert a supported stint-time value into timedelta."""
    if isinstance(value, timedelta):
        return value

    if isinstance(value, (int, float)):
        return timedelta(seconds=float(value))

    if isinstance(value, str):
        text = value.strip()
        if not text:
            return timedelta(0)

        parts = text.split(':')
        if len(parts) == 3:
            try:
                hours = int(parts[0])
                minutes = int(parts[1])
                seconds = float(parts[2])
                return timedelta(hours=hours, minutes=minutes, seconds=seconds)
            except Exception:
                return timedelta(0)

        try:
            return timedelta(seconds=float(text))
        except Exception:
            return timedelta(0)

    return timedelta(0)


def _get_longest_stint(context: dict = None) -> str:
    """Return the longest completed stint as an HH:MM:SS string.

    Expected context shape:
        {"table_model": <TableModel instance>}
    """
    context_data = context or {}
    table_model = context_data.get("table_model")

    if table_model is None:
        log(
            'DEBUG',
            'TableModel missing in stats context; returning default longest stint',
            category='stats_strip',
            action='get_longest_stint',
        )
        return format_stint_time(timedelta(0))

    rows = getattr(table_model, '_data', []) or []
    longest = timedelta(0)

    for row in rows:
        try:
            status = str(row[ColumnIndex.STATUS])
            if 'Completed' not in status:
                continue

            current = _parse_stint_time(row[ColumnIndex.STINT_TIME])
            if current > longest:
                longest = current
        except Exception:
            continue

    return format_stint_time(longest)
