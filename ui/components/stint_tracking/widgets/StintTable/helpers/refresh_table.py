from __future__ import annotations

from PyQt6.QtWidgets import QApplication


def refresh_table(self, skip_model_update: bool = False) -> None:
    """Refresh data and column configuration."""
    if self.table_model is None:
        return

    if isinstance(skip_model_update, str):
        skip_model_update = False

    app_window = self.window() or (QApplication.instance().activeWindow() if QApplication.instance() else None)
    if not skip_model_update and app_window and hasattr(app_window, 'show_loading'):
        app_window.show_loading('Loading session data...')

    if not skip_model_update:
        try:
            self.table_model.update_data()
        finally:
            if app_window and hasattr(app_window, 'hide_loading'):
                app_window.hide_loading()
    else:
        if app_window and hasattr(app_window, 'hide_loading'):
            app_window.hide_loading()

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
