"""Build per-driver stats for the StatsStrip."""

from __future__ import annotations

from datetime import timedelta

from core.database import get_team

from ui.models.stint_helpers import format_timedelta
from ui.models.table_constants import ColumnIndex

from ._parse_duration_seconds import _parse_duration_seconds


def _get_driver_stats(table_model) -> list[dict[str, int | str]]:
    """Return ordered driver stats derived from completed table rows."""
    rows, _, _ = table_model.get_all_data()
    team = get_team() or {}
    team_drivers = [
        driver.strip()
        for driver in team.get('drivers', [])
        if isinstance(driver, str) and driver.strip()
    ]

    stats_by_driver: dict[str, dict[str, int | str]] = {
        driver_name: {
            'driver_name': driver_name,
            'stint_count': 0,
            'total_seconds': 0,
        }
        for driver_name in team_drivers
    }

    total_seconds = 0

    for row in rows:
        if len(row) <= ColumnIndex.STINT_TIME:
            continue

        status = str(row[ColumnIndex.STATUS]).strip().lower()
        if status != 'completed':
            continue

        driver_cell = row[ColumnIndex.DRIVER]
        if driver_cell is None:
            continue

        driver_name = str(driver_cell).strip()
        if not driver_name:
            continue

        stint_seconds = _parse_duration_seconds(str(row[ColumnIndex.STINT_TIME]))
        total_seconds += stint_seconds

        if driver_name not in stats_by_driver:
            stats_by_driver[driver_name] = {
                'driver_name': driver_name,
                'stint_count': 0,
                'total_seconds': 0,
            }

        stats_by_driver[driver_name]['stint_count'] += 1
        stats_by_driver[driver_name]['total_seconds'] += stint_seconds

    driver_stats: list[dict[str, int | str]] = []
    for driver_stat in stats_by_driver.values():
        driver_seconds = int(driver_stat['total_seconds'])
        progress_value = 0
        if total_seconds > 0:
            progress_value = round((driver_seconds / total_seconds) * 100)

        total_time_text = '—' if driver_seconds == 0 else format_timedelta(
            timedelta(seconds=driver_seconds)
        )

        driver_stats.append({
            'driver_name': str(driver_stat['driver_name']),
            'stint_count': int(driver_stat['stint_count']),
            'total_time_text': total_time_text,
            'progress_value': progress_value,
        })

    return driver_stats