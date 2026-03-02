"""Pad button text to add horizontal spacing."""

from PyQt6.QtGui import QFontMetrics


def _pad_text(self, text: str, gap: int = 1) -> str:
    """Return text prefixed with spaces to achieve a pixel gap."""
    if not text:
        return text
    fm = QFontMetrics(self.btn.font())
    space_width = fm.boundingRect(' ').width() or 1
    count = (gap + space_width - 1) // space_width
    return ' ' * count + text
