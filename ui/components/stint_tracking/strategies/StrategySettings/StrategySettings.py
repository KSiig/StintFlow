"""Strategy settings widget for strategy tabs."""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from ui.models import ModelContainer
from ui.utilities.load_style import load_style

from .helpers import (
    _apply_input_state,
    _capture_input_state,
    _create_labeled_input_rows,
    _data_changed,
    _handle_save_shortcut,
    _on_cancel_clicked,
    _on_delete_clicked,
    _on_save_clicked,
    _realign_rows,
    _set_inputs,
    _setup_ui,
)


class StrategySettings(QWidget):
    """Placeholder widget for strategy settings/info box."""

    strategy_updated = pyqtSignal(dict)
    strategy_deleted = pyqtSignal(str)

    _setup_ui = _setup_ui
    _apply_input_state = _apply_input_state
    _capture_input_state = _capture_input_state
    _create_labeled_input_rows = _create_labeled_input_rows
    _handle_save_shortcut = _handle_save_shortcut
    _on_save_clicked = _on_save_clicked
    _on_cancel_clicked = _on_cancel_clicked
    _on_delete_clicked = _on_delete_clicked
    _realign_rows = _realign_rows
    _set_inputs = _set_inputs
    _data_changed = _data_changed

    def __init__(self, parent=None, models: ModelContainer = None, strategy=None):
        super().__init__(parent)

        self.selection_model = models.selection_model if models else None
        self.table_model = models.table_model if models else None
        self.inputs: dict = {}
        self.strategy = strategy
        self._committed_input_state: dict[str, str | bool] | None = None
        self._has_unsaved_input_changes = False
        self._is_restoring_input_state = False

        load_style('resources/styles/stint_tracking/strategy_settings.qss', widget=self)
        self._setup_ui()

        if self.table_model is not None:
            self.table_model.dataChanged.connect(self._data_changed)
