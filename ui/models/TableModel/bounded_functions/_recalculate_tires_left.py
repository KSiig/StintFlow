"""Delegate remaining‑tires calculation to shared processor."""

from ui.models.table_processors import recalculate_tires_left


def _recalculate_tires_left(self) -> None:
    """Recalculate remaining tires for all rows based on tire changes."""
    recalculate_tires_left(
        self._data,
        self._tires,
        self._event_tire_count,
        self._recalculate_stint_types,
    )
