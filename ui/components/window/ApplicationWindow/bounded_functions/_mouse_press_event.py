from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent
from PyQt6.QtWidgets import QMainWindow


def mousePressEvent(self, event: QMouseEvent) -> None:
    """Handle mouse press events to start edge resizing."""
    if event.button() == Qt.MouseButton.LeftButton:
        edge = self.resize_controller.get_resize_edge(event.position().toPoint())
        if edge:
            self.resize_controller.start_resize(edge, event.globalPosition().toPoint())
            event.accept()
            return

    QMainWindow.mousePressEvent(self, event)
