"""Configuration view for stint tracking."""

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget

from ui.models import ModelContainer

from .bounded_functions import closeEvent
from .helpers import (
    _create_table_controls,
    _on_tracker_started,
    _on_tracker_stopped,
    _setup_ui,
    _start_polling_timer,
    _startup_tick,
    _toggle_left_column,
)


class ConfigView(QWidget):
    """View for stint tracking configuration."""

    SPACING = 16

    _create_table_controls = _create_table_controls
    _setup_ui = _setup_ui
    _on_tracker_started = _on_tracker_started
    _on_tracker_stopped = _on_tracker_stopped
    _startup_tick = _startup_tick
    _start_polling_timer = _start_polling_timer
    _toggle_left_column = _toggle_left_column
    closeEvent = closeEvent

    def __init__(self, models: ModelContainer) -> None:
        super().__init__()
        self.selection_model = models.selection_model
        self.table_model = models.table_model
        self.config_options = None
        self.agent_overview = None
        self.stint_table = None
        self._startup_timer = None
        self._startup_count = 0
        self._poll_timer = None
        self.inputs: dict[str, QLineEdit] = {}
        self.status_label: QLabel | None = None
        self.reload_button: QPushButton | None = None

        self._setup_ui(models)
