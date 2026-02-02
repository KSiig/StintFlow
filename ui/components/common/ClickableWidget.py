"""
Clickable widget that triggers a callback when clicked.

Simple wrapper widget that makes any content clickable.
"""

from typing import Callable
from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QMouseEvent


class ClickableWidget(QWidget):
    """
    Widget that triggers a callback when clicked.
    
    Wraps another widget or layout and makes it clickable.
    """
    
    def __init__(self, callback: Callable, parent: QWidget = None):
        """
        Initialize the clickable widget.
        
        Args:
            callback: Function to call when widget is clicked
            parent: Parent widget
        """
        super().__init__(parent)
        self.callback = callback
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
    
    def mousePressEvent(self, event: QMouseEvent) -> None:
        """
        Handle mouse press events.
        
        Args:
            event: Mouse press event
        """
        if event.button() == Qt.MouseButton.LeftButton:
            self.callback()
            event.accept()
        else:
            super().mousePressEvent(event)
