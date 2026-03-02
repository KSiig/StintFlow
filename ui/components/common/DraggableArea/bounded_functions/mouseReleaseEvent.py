"""Mouse release handler for draggable window area."""

from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget


def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Reset drag tracking when the mouse button is released."""
    self._initial_pos = None
    self._was_maximized = False

    QWidget.mouseReleaseEvent(self, event)
    event.accept()
