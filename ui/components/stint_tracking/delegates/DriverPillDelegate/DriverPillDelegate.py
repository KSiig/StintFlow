"""Delegate for rendering driver names as pills."""

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QStyledItemDelegate

from .helpers import _paint


class DriverPillDelegate(QStyledItemDelegate):
    """Render driver text inside pill-shaped backgrounds."""

    paint = _paint

    def __init__(self, parent=None, background_color: str = "#0e4c35", text_color: str = "#ffffff") -> None:
        super().__init__(parent)
        self.background_color = QColor(background_color)
        self.text_color = QColor(text_color)
        self.border_radius = 12
        self.padding_horizontal = 12
        self.padding_vertical = 4
        self.left_margin = 8
