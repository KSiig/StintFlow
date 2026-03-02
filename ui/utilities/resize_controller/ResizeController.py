"""Window resize controller for frameless windows."""

from PyQt6.QtCore import QPoint, QRect, Qt
from PyQt6.QtWidgets import QMainWindow


class ResizeController:
    """Manages edge and corner resizing for frameless windows."""

    def __init__(self, window: QMainWindow, edge_margin: int = 8):
        self.window = window
        self.edge_margin = edge_margin
        self._resize_start_pos: QPoint | None = None
        self._resize_start_geometry: QRect | None = None
        self._resize_edge: str | None = None

    def get_resize_edge(self, pos: QPoint) -> str | None:
        """Determine which edge or corner is near the mouse position."""
        if self.window.isMaximized():
            return None

        rect = self.window.rect()
        at_left = pos.x() <= self.edge_margin
        at_right = pos.x() >= rect.width() - self.edge_margin
        at_bottom = pos.y() >= rect.height() - self.edge_margin

        if at_bottom and at_left:
            return "bottom-left"
        if at_bottom and at_right:
            return "bottom-right"
        if at_left:
            return "left"
        if at_right:
            return "right"
        if at_bottom:
            return "bottom"
        return None

    def update_cursor(self, edge: str | None = None) -> None:
        """Update the cursor to reflect the active resize edge."""
        if edge == "bottom-left":
            self.window.setCursor(Qt.CursorShape.SizeBDiagCursor)
        elif edge == "bottom-right":
            self.window.setCursor(Qt.CursorShape.SizeFDiagCursor)
        elif edge in ("left", "right"):
            self.window.setCursor(Qt.CursorShape.SizeHorCursor)
        elif edge == "bottom":
            self.window.setCursor(Qt.CursorShape.SizeVerCursor)
        else:
            self.window.setCursor(Qt.CursorShape.ArrowCursor)

    def start_resize(self, edge: str, global_pos: QPoint) -> None:
        """Begin a resize operation from ``edge`` at ``global_pos``."""
        self._resize_edge = edge
        self._resize_start_pos = global_pos
        self._resize_start_geometry = self.window.geometry()

    def is_resizing(self) -> bool:
        """Return True if a resize operation is active."""
        return self._resize_start_pos is not None

    def update_resize(self, global_pos: QPoint) -> None:
        """Update window geometry during an active resize."""
        if not self.is_resizing():
            return

        delta = global_pos - self._resize_start_pos
        new_geometry = QRect(self._resize_start_geometry)

        if self._resize_edge == "left":
            new_geometry.setLeft(self._resize_start_geometry.left() + delta.x())
        elif self._resize_edge == "right":
            new_geometry.setRight(self._resize_start_geometry.right() + delta.x())
        elif self._resize_edge == "bottom":
            new_geometry.setBottom(self._resize_start_geometry.bottom() + delta.y())
        elif self._resize_edge == "bottom-left":
            new_geometry.setLeft(self._resize_start_geometry.left() + delta.x())
            new_geometry.setBottom(self._resize_start_geometry.bottom() + delta.y())
        elif self._resize_edge == "bottom-right":
            new_geometry.setRight(self._resize_start_geometry.right() + delta.x())
            new_geometry.setBottom(self._resize_start_geometry.bottom() + delta.y())

        self.window.setGeometry(new_geometry)

    def stop_resize(self) -> None:
        """End the current resize operation."""
        self._resize_edge = None
        self._resize_start_pos = None
        self._resize_start_geometry = None
