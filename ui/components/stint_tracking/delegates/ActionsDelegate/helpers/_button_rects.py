"""Compute button rectangles for the actions column."""

from PyQt6.QtCore import QRect


def _button_rects(self, option_rect: QRect) -> list[QRect]:
    """Return rects for each configured button laid out horizontally."""
    rects: list[QRect] = []
    x = option_rect.left() + self.spacing
    height = self.button_width
    y = option_rect.top() + option_rect.height() // 2 - height // 2

    for _ in self.buttons:
        rects.append(QRect(x, y, self.button_width, height))
        x += self.button_width + self.spacing

    return rects
