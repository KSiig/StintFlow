"""Controls bar displayed above the stint table in ConfigView."""

from __future__ import annotations

from PyQt6.QtWidgets import QWidget

from .helpers import _apply_tracking_state, _setup_ui
from ui.utilities.load_style import load_style


class TableControls(QWidget):
    """Horizontal bar holding the left-column toggle and tracking buttons.

    Args:
        config_options: The ConfigOptions widget whose tracker signals and
            buttons this widget mirrors and drives.
        on_toggle_left_column: Callback invoked when the hide/show toggle
            button is clicked.
    """

    _setup_ui = _setup_ui
    _apply_tracking_state = _apply_tracking_state

    def __init__(self, config_options, on_toggle_left_column: callable) -> None:
        # config_options is not typed strictly to avoid a circular import
        # (TableControls lives alongside ConfigOptions in the widgets package).
        super().__init__()
        load_style('resources/styles/stint_tracking/config_options/table_controls.qss', widget=self)

        self.config_options = config_options
        self._on_toggle_left_column = on_toggle_left_column
        self._left_column_toggle_btn = None
        self.tracking_btn = None

        self._setup_ui()
