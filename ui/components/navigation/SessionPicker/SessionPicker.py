"""
Event and session selection widget using dropdown buttons.
"""

from PyQt6.QtWidgets import QWidget

from ui.models import ModelContainer

from .bounded_functions import reload
from .helpers import (
    _add_combo_icon,
    _apply_selection_from_model,
    _create_combo_box,
    _create_layout,
    _load_events,
    _on_event_changed,
    _on_session_changed,
    _populate_initial_data,
    _populate_sessions,
    _setup_styles,
)


class SessionPicker(QWidget):
    """Event and session selection widget."""

    reload = reload

    _setup_styles = _setup_styles
    _create_layout = _create_layout
    _create_combo_box = _create_combo_box
    _add_combo_icon = _add_combo_icon
    _populate_initial_data = _populate_initial_data
    _load_events = _load_events
    _apply_selection_from_model = _apply_selection_from_model
    _populate_sessions = _populate_sessions
    _on_event_changed = _on_event_changed
    _on_session_changed = _on_session_changed

    def __init__(self, models: ModelContainer = None) -> None:
        super().__init__()
        self.models = models
        self.selection_model = models.selection_model if models else None

        self._setup_styles()
        self._create_layout()
        # Data loading is deferred; caller should invoke reload() when ready.
