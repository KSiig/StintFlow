"""Strategies view for managing race strategies."""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QWidget

from ui.models import ModelContainer

from .helpers import (
    _add_tab,
    _clear_tabs,
    _create_strategy_tab,
    _load_strategies,
    _on_clone_strategy,
    _on_create_strategy,
    _on_session_changed,
    _on_strategy_created,
    _on_tab_changed,
    _remove_tab,
    _setup_styles,
    _setup_ui,
    _update_tab_label,
)


class StrategiesView(QWidget):
    """Main view for race strategy management."""

    strategy_created = pyqtSignal(dict)

    _setup_styles = _setup_styles
    _setup_ui = _setup_ui
    _on_tab_changed = _on_tab_changed
    _load_strategies = _load_strategies
    _create_strategy_tab = _create_strategy_tab
    _on_strategy_created = _on_strategy_created
    _on_create_strategy = _on_create_strategy
    _on_clone_strategy = _on_clone_strategy
    _on_session_changed = _on_session_changed
    _clear_tabs = _clear_tabs
    _remove_tab = _remove_tab
    _update_tab_label = _update_tab_label
    _add_tab = _add_tab

    def __init__(self, models: ModelContainer):
        super().__init__()

        self.models = models
        self.selection_model = models.selection_model
        self.table_model = models.table_model

        self.main_layout = None
        self.tab_bar = None
        self.stacked_widget = None

        self.selection_model.sessionChanged.connect(self._on_session_changed)

        self._setup_ui()
        self._setup_styles()
        self._load_strategies()
