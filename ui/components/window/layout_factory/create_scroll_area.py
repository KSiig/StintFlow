from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QScrollArea


def create_scroll_area() -> QScrollArea:
    """Create a scrollable content area for the main workspace."""
    scroll_area = QScrollArea()
    scroll_area.setWidgetResizable(True)
    scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    scroll_area.setFrameShape(QFrame.Shape.NoFrame)
    return scroll_area
