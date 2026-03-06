"""Get mean stint time from the table model context."""

from __future__ import annotations

from datetime import timedelta

from core.errors import log
from core.utilities import format_stint_time


def _get_avg_stint_time(context: dict = None) -> timedelta:
  """Return the current mean stint time from TableModel.

  Expected context shape:
    {"table_model": <TableModel instance>}
  """
  context_data = context or {}
  table_model = context_data.get("table_model")

  if table_model is None:
    log(
      'DEBUG',
      'TableModel missing in stats context; returning default mean stint time',
      category='stats_strip',
      action='get_avg_stint_time',
    )
    return timedelta(0)

  mean_stint_time = getattr(table_model, '_mean_stint_time', timedelta(0))
  print("mean_stint_time:", mean_stint_time)  # Debug print
  if mean_stint_time is None:
    return timedelta(0)

  return format_stint_time(mean_stint_time)

