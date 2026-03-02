from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QMainWindow


def mouseReleaseEvent(self, event: QMouseEvent) -> None:
    """Handle mouse release events to stop edge resizing."""
    if event.button() == Qt.MouseButton.LeftButton and self.resize_controller.is_resizing():
        self.resize_controller.stop_resize()
        edge = self.resize_controller.get_resize_edge(event.position().toPoint())
        self.resize_controller.update_cursor(edge)
        event.accept()
        return

    QMainWindow.mouseReleaseEvent(self, event)
