from PyQt6.QtCore import QEvent
from PyQt6.QtWidgets import QMainWindow, QWidget


def eventFilter(self, obj: QWidget, event: QEvent) -> bool:
    """Update resize cursor when hovering over edges of child widgets."""
    if not isinstance(obj, QWidget) or (not self.isAncestorOf(obj) and obj != self):
        return QMainWindow.eventFilter(self, obj, event)

    if event.type() == QEvent.Type.MouseMove and not self.resize_controller.is_resizing():
        global_pos = event.globalPosition().toPoint()
        window_pos = self.mapFromGlobal(global_pos)
        if self.rect().contains(window_pos):
            edge = self.resize_controller.get_resize_edge(window_pos)
            self.resize_controller.update_cursor(edge)

    elif event.type() == QEvent.Type.Leave and not self.resize_controller.is_resizing():
        self.unsetCursor()

    return QMainWindow.eventFilter(self, obj, event)
