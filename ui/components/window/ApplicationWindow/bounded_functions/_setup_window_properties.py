from PyQt6.QtCore import Qt

from ...constants import WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_X, WINDOW_Y


def _setup_window_properties(self) -> None:
    """Configure basic window properties (size, flags, style)."""
    self.setGeometry(WINDOW_X, WINDOW_Y, WINDOW_WIDTH, WINDOW_HEIGHT)
    self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
