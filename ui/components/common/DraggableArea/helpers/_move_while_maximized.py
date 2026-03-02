"""Helper to restore a maximized window and continue dragging."""

from PyQt6.QtCore import QPoint
from PyQt6.QtGui import QMouseEvent


def _move_while_maximized(self, event: QMouseEvent) -> None:
    """Restore a maximized window and position it under the cursor for drag."""
    global_pos = event.globalPosition().toPoint()

    window = self.window()
    window.showNormal()

    window_width = window.width()
    click_ratio = self._initial_pos.x() / self.width()
    offset_x = int(window_width * click_ratio)

    new_x = global_pos.x() - offset_x
    new_y = global_pos.y() - self._initial_pos.y()
    window.move(new_x, new_y)

    self._initial_pos = QPoint(offset_x, self._initial_pos.y())
    self._was_maximized = False
