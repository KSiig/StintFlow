"""
Clickable widget that triggers a callback when clicked.

Simple wrapper widget that makes any content clickable.
"""

from typing import Callable
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

from .bounded_functions import mousePressEvent


ClickCallback = Callable[[], None]


class ClickableWidget(QWidget):
    """
    Widget that triggers a callback when clicked.

    Wraps another widget or layout and makes it clickable.
    """

    mousePressEvent = mousePressEvent

    def __init__(self, callback: ClickCallback, parent: QWidget = None):
        """
        Initialize the clickable widget.

        Args:
            callback: Function called on left-click.
            parent: Parent widget.
        """
        super().__init__(parent)
        self.callback = callback
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
