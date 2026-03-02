from __future__ import annotations

from PyQt6.QtWidgets import QWidget

from .bounded_functions._create_button import _create_button
from .bounded_functions._create_layout import _create_layout
from .bounded_functions._get_restart_command import _get_restart_command
from .bounded_functions._restart_app import _restart_app
from .bounded_functions._should_show_restart import _should_show_restart
from .bounded_functions.window_state_changed import window_state_changed


class WindowButtons(QWidget):
    """Window control buttons (minimize, maximize/restore, restart, close)."""

    BUTTON_SIZE = 28
    BUTTON_ICON_SIZE = 16
    BUTTON_SPACING = 4
    BUTTON_CONTAINER_MARGIN_TOP = 8
    BUTTON_CONTAINER_MARGIN_RIGHT = 0

    BUTTON_ICONS = {
        "minimize": "resources/icons/window_buttons/minus.svg",
        "maximize": "resources/icons/window_buttons/square.svg",
        "restore": "resources/icons/window_buttons/restore.svg",
        "restart": "resources/icons/window_buttons/restart.svg",
        "close": "resources/icons/window_buttons/x.svg",
    }

    _create_button = _create_button
    _create_layout = _create_layout
    _get_restart_command = _get_restart_command
    _restart_app = _restart_app
    _should_show_restart = _should_show_restart
    window_state_changed = window_state_changed

    def __init__(self, parent):
        super().__init__(parent)
        self.initial_pos = None
        self._create_layout()
