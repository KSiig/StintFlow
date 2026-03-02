"""Helper to move a window while dragging in normal state."""

from PyQt6.QtGui import QMouseEvent


def _move_while_normal(self, event: QMouseEvent) -> None:
    """Move the window using cursor delta from the initial click position."""
    delta = event.position().toPoint() - self._initial_pos
    window = self.window()
    window.move(
        window.x() + delta.x(),
        window.y() + delta.y(),
    )
