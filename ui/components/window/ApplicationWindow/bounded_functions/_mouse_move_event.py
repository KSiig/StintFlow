from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QMainWindow


def mouseMoveEvent(self, event: QMouseEvent) -> None:
    """Handle mouse move events for resize cursor and resize action."""
    if self.resize_controller.is_resizing():
        self.resize_controller.update_resize(event.globalPosition().toPoint())
    else:
        edge = self.resize_controller.get_resize_edge(event.position().toPoint())
        self.resize_controller.update_cursor(edge)

    QMainWindow.mouseMoveEvent(self, event)
