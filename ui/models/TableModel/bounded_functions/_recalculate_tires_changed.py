"""Delegate tires‑changed recalculation to table processor."""

from ui.models.table_processors import recalculate_tires_changed


def _recalculate_tires_changed(self, index, old_value: str) -> None:
    """Recalculate tire changes after stint type edit."""
    recalculate_tires_changed(
        self._data,
        self._tires,
        index.row(),
        old_value,
        self.rowCount(),
        self._recalculate_tires_left,
    )
