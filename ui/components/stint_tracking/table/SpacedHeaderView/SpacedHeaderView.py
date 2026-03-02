"""Custom horizontal header view with configurable icon spacing."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHeaderView

from .helpers import paint_section


class SpacedHeaderView(QHeaderView):
    """Horizontal header view that adjusts icon/text spacing."""

    paintSection = paint_section

    def __init__(
        self,
        orientation=Qt.Orientation.Horizontal,
        parent=None,
        icon_text_spacing: int = 8,
        left_padding: int = 8,
    ) -> None:
        super().__init__(orientation, parent)
        self.icon_text_spacing = icon_text_spacing
        self.left_padding = left_padding
        self.icon_size = 16
