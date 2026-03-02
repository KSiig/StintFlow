"""Strategy settings widget for strategy tabs."""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from ui.models import ModelContainer
from ui.utilities.load_style import load_style

from .helpers import (
    _create_labeled_input_rows,
    _data_changed,
    _format_stint_time,
    _on_delete_clicked,
    _on_save_clicked,
    _realign_rows,
    _set_inputs,
    _setup_ui,
    _toggle_edit,
)


class StrategySettings(QWidget):
    """Placeholder widget for strategy settings/info box."""

    strategy_updated = pyqtSignal(dict)
    strategy_deleted = pyqtSignal(str)

    _setup_ui = _setup_ui
    _create_labeled_input_rows = _create_labeled_input_rows
    _toggle_edit = _toggle_edit
    _on_save_clicked = _on_save_clicked
    _on_delete_clicked = _on_delete_clicked
    _realign_rows = _realign_rows
    _set_inputs = _set_inputs
    _format_stint_time = _format_stint_time
    _data_changed = _data_changed

    def __init__(self, parent=None, models: ModelContainer = None, strategy=None):
        super().__init__(parent)

        self.selection_model = models.selection_model if models else None
        self.table_model = models.table_model if models else None
        self.inputs: dict = {}
        self.strategy = strategy

        load_style('resources/styles/stint_tracking/strategy_settings.qss', widget=self)
        self._setup_ui()

        if self.table_model is not None:
            self.table_model.dataChanged.connect(self._data_changed)
