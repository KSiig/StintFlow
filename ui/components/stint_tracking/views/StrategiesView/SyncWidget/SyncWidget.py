"""Sync control shown in the StrategiesView header row."""

from __future__ import annotations

from PyQt6.QtCore import QTimer, pyqtSignal
from PyQt6.QtWidgets import QWidget, QLabel, QCheckBox, QFrame

from ui.utilities.load_style import load_style

from .helpers import (
    _get_auto_sync_interval_seconds,
    _handle_auto_sync_toggled,
    _setup_ui,
    _update_auto_sync_icon,
)


class SyncWidget(QWidget):
    """Header widget that exposes sync actions for strategy data.

    The widget presents manual and automatic sync controls for the active
    strategy tab. Automatic sync emits the same sync signal on a configurable
    timer read from user settings.
    """

    sync_requested = pyqtSignal()

    _setup_ui = _setup_ui
    _update_auto_sync_icon = _update_auto_sync_icon
    _handle_auto_sync_toggled = _handle_auto_sync_toggled
    _get_auto_sync_interval_seconds = _get_auto_sync_interval_seconds

    def __init__(self) -> None:
        super().__init__()

        self.auto_sync_frame: QFrame | None = None
        self.auto_sync_icon_label: QLabel | None = None
        self.auto_sync_text_label: QLabel | None = None
        self.auto_sync_toggle: QCheckBox | None = None
        self.manual_sync_frame: QFrame | None = None
        self.icon_label: QLabel | None = None
        self.text_label: QLabel | None = None
        self._auto_sync_timer = QTimer(self)
        self._auto_sync_timer.timeout.connect(self.sync_requested.emit)

        self._setup_ui()
        load_style('resources/styles/stint_tracking/sync_widget.qss', widget=self)
        self._update_auto_sync_icon(False)
