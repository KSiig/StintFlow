"""Strategy display tab showing editable strategy tables."""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from ui.models import SelectionModel, TableModel
from ui.utilities.load_style import load_style

from .helpers import (
    _load_strategy_data,
    _on_delete_clicked,
    _on_exclude_clicked,
    _on_settings_deleted,
    _open_persistent_editors,
    _setup_strategy_delegates,
    _setup_ui,
    _sync_from_tracker,
    _strategy_updated,
)


class StrategyTab(QWidget):
    """Tab displaying an existing race strategy."""

    name_changed = pyqtSignal(str)
    deleted = pyqtSignal(str)

    _setup_ui = _setup_ui
    _load_strategy_data = _load_strategy_data
    _setup_strategy_delegates = _setup_strategy_delegates
    _open_persistent_editors = _open_persistent_editors
    _strategy_updated = _strategy_updated
    _on_settings_deleted = _on_settings_deleted
    _on_delete_clicked = _on_delete_clicked
    _on_exclude_clicked = _on_exclude_clicked
    _sync_from_tracker = _sync_from_tracker

    def __init__(self, strategy: dict, table_model: TableModel, selection_model: SelectionModel):
        """Initialize a strategy tab with a cloned strategy model and tracker source model."""
        super().__init__()

        self.strategy = strategy
        self.strategy_id = strategy.get('_id')
        self.strategy_name = strategy.get('name', 'Unnamed Strategy')
        self.selection_model = selection_model
        self.tracker_table_model = table_model

        self.table_model = table_model.clone()
        self.table_model._is_strategy = True
        self._lock_completed = False

        load_style('resources/styles/stint_tracking/strategy_tab.qss', widget=self)
        self._setup_ui()
        self._load_strategy_data()
