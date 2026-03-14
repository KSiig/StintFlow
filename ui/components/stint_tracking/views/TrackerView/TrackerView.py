"""Tracker view for managing stint tracking state and data."""

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget

from ui.models import ModelContainer

from .bounded_functions import closeEvent
from .helpers import (
    _animate_left_column,
    _install_viewport_listener,
    _on_resize,
    _on_show,
    _on_tracker_started,
    _on_tracker_stopped,
    _setup_ui,
    _sync_top_row_heights,
    _start_polling_timer,
    _startup_tick,
    _toggle_left_column,
    _update_controls_width,
)


class TrackerView(QWidget):
    """Primary tracker view for state control, configuration, and data."""

    SPACING = 16

    _animate_left_column = _animate_left_column
    _setup_ui = _setup_ui
    _on_resize = _on_resize
    _update_controls_width = _update_controls_width
    _sync_top_row_heights = _sync_top_row_heights
    _install_viewport_listener = _install_viewport_listener
    _on_show = _on_show
    resizeEvent = _on_resize
    showEvent = _on_show
    _on_tracker_started = _on_tracker_started
    _on_tracker_stopped = _on_tracker_stopped
    _startup_tick = _startup_tick
    _start_polling_timer = _start_polling_timer
    _toggle_left_column = _toggle_left_column
    closeEvent = closeEvent

    def __init__(self, models: ModelContainer) -> None:
        super().__init__()
        self.models = models
        self.selection_model = models.selection_model
        self.table_model = models.table_model
        self.config_options = None
        self.agent_overview = None
        self.stint_table = None
        self.stats_strip = None
        self.table_controls = None
        self.left_column_container = None
        self.right_column_container = None
        self._left_column_animation = None
        self._left_column_expanded_width = 0
        self._viewport_filter = None
        self._startup_timer = None
        self._startup_count = 0
        self._poll_timer = None
        self.inputs: dict[str, QLineEdit] = {}
        self.status_label: QLabel | None = None
        self.reload_button: QPushButton | None = None

        self._setup_ui(models)
