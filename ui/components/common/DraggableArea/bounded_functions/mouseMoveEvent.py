"""Mouse move handler for draggable window area."""

from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget


def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """Move the window while dragging, including maximize-to-normal transition."""
    if self._initial_pos is not None:
        if self._was_maximized:
            self._move_while_maximized(event)
        else:
            self._move_while_normal(event)

    QWidget.mouseMoveEvent(self, event)
    event.accept()
