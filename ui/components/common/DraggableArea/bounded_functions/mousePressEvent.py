"""Mouse press handler for draggable window area."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget


def mousePressEvent(self, event: QMouseEvent) -> None:
    """Capture initial drag position when left mouse button is pressed."""
    if event.button() == Qt.MouseButton.LeftButton:
        self._initial_pos = event.position().toPoint()
        self._was_maximized = self.window().isMaximized()

    QWidget.mousePressEvent(self, event)
    event.accept()
