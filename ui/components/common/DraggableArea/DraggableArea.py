"""
Draggable area widget for moving the main window.

An invisible overlay widget positioned absolutely at the top of the window
that allows users to click and drag to move the window. Does not participate
in any layout and doesn't affect other component positioning.
"""

from PyQt6.QtCore import Qt, QPoint
from PyQt6.QtWidgets import QWidget

from .bounded_functions import (
    mouseMoveEvent,
    mousePressEvent,
    mouseReleaseEvent,
)
from .helpers import (
    _move_while_maximized,
    _move_while_normal,
)


class DraggableArea(QWidget):
    """
    Invisible widget that enables window dragging when clicked.
    
    This widget is positioned absolutely at the top of the main window
    and captures mouse events to allow the user to move the frameless window.
    """

    mousePressEvent = mousePressEvent
    mouseMoveEvent = mouseMoveEvent
    mouseReleaseEvent = mouseReleaseEvent

    _move_while_maximized = _move_while_maximized
    _move_while_normal = _move_while_normal

    def __init__(self, parent: QWidget):
        """Initialize the draggable area and drag state."""
        super().__init__(parent)
        self._initial_pos: QPoint = None
        self._was_maximized: bool = False

        # Make the widget invisible but still capture mouse events
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setStyleSheet("background-color: transparent;")
