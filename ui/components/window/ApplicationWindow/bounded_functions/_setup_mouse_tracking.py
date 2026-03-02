from PyQt6.QtWidgets import QWidget


def _setup_mouse_tracking(self) -> None:
    """Enable mouse tracking for resize cursor updates."""
    self.setMouseTracking(True)
    for child in self.findChildren(QWidget):
        if child.parent() == self:
            child.setMouseTracking(True)
