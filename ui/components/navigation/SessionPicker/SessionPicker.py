"""
Event and session selection widget using dropdown buttons.
"""

from PyQt6.QtWidgets import QSizePolicy, QWidget

from ui.models import ModelContainer
from ui.utilities.load_style import load_style

from .bounded_functions import reload
from .helpers import (
    _add_combo_icon,
    _apply_selection_from_model,
    _can_change_selection,
    _create_combo_box,
    _create_layout,
    _load_events,
    _on_event_changed,
    _on_session_changed,
    _populate_initial_data,
    _populate_sessions,
)


class SessionPicker(QWidget):
    """Event and session selection widget."""

    reload = reload

    _create_layout = _create_layout
    _create_combo_box = _create_combo_box
    _add_combo_icon = _add_combo_icon
    _populate_initial_data = _populate_initial_data
    _load_events = _load_events
    _apply_selection_from_model = _apply_selection_from_model
    _can_change_selection = _can_change_selection
    _populate_sessions = _populate_sessions
    _on_event_changed = _on_event_changed
    _on_session_changed = _on_session_changed

    def __init__(self, models: ModelContainer = None) -> None:
        super().__init__()
        self.models = models
        self.selection_model = models.selection_model if models else None

        load_style('resources/styles/navigation/session_picker.qss', widget=self)
        self.setObjectName("StintSelection")
        self.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
        self._create_layout()
        # Data loading is deferred; caller should invoke reload() when ready.
