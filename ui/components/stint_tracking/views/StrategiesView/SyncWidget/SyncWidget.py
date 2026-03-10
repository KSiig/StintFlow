"""Sync control shown in the StrategiesView header row."""

from __future__ import annotations

from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtWidgets import QWidget, QLabel

from ui.utilities.load_style import load_style

from .helpers import _setup_ui


class SyncWidget(QWidget):
    """Header widget that exposes sync actions for strategy data.

    The widget currently presents a clickable area containing an icon and
    a text label.  Using a custom QWidget allows precise control over the
    layout and spacing of the two elements.
    """

    sync_requested = pyqtSignal()

    _setup_ui = _setup_ui

    def __init__(self) -> None:
        super().__init__()

        self.icon_label: QLabel | None = None
        self.text_label: QLabel | None = None

        self._setup_ui()
        load_style('resources/styles/stint_tracking/sync_widget.qss', widget=self)

        # clickable cursor
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def mousePressEvent(self, event) -> None:
        super().mousePressEvent(event)
        self.sync_requested.emit()
