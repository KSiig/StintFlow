"""Mouse press handler for the clickable widget component."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QWidget

def mousePressEvent(self, event: QMouseEvent) -> None:
    """
    Handle mouse press events for the clickable widget.

    Left-click invokes the widget callback and consumes the event.
    Any other mouse button is delegated to the parent implementation.

    Args:
        event: The incoming mouse press event.
    """
    is_left_click = event.button() == Qt.MouseButton.LeftButton
    if not is_left_click:
        QWidget.mousePressEvent(self, event)
        return

    self.callback()
    event.accept()