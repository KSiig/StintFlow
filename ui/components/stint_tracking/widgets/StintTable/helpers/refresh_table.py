from __future__ import annotations

from ui.utilities.loading_queue import LoadingQueue

MESSAGE = "Loading session data..."


def refresh_table(self, skip_model_update: bool = False) -> None:
    """Refresh data and column configuration."""
    if self.table_model is None:
        return

    if isinstance(skip_model_update, str):
        skip_model_update = False

    if not skip_model_update:
        LoadingQueue.push(MESSAGE)
        try:
            self.table_model.update_data()
        finally:
            LoadingQueue.pop(MESSAGE)

    if self.table_model.rowCount() == 0:
        self._show_placeholder()
    else:
        self._hide_placeholder()

    if self.table.model():
        column_count = self.table.model().columnCount()
        if self._column_count != column_count:
            self._set_column_widths()

    if self.table.model() is None:
        self.table.setModel(self.table_model)
        if self.table.model() is not None:
            self._column_count = self.table.model().columnCount()
            self._set_column_widths()
