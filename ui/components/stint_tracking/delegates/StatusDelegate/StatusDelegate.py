"""Delegate for rendering status values with icons."""

from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QStyledItemDelegate

from .helpers import _paint


class StatusDelegate(QStyledItemDelegate):
    """Render status text with icons and colors."""

    STATUS_CONFIG = {
        "Completed": ("circle-check.svg", "#05fd7e"),
        "Pending": ("hourglass.svg", "#cf8b3c"),
    }

    paint = _paint

    def __init__(self, parent=None, icon_size: int = 16, icon_text_spacing: int = 6, left_margin: int = 8) -> None:
        super().__init__(parent)
        self.icon_size = icon_size
        self.icon_text_spacing = icon_text_spacing
        self.left_margin = left_margin
        self.default_color = QColor("#ffffff")
