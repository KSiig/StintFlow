"""Draw a pill-style button with optional icon or text."""

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QColor

from ui.utilities.load_icon import load_icon


def _draw_button(self, painter, style, rect: QRect, svg_name: str | None = None, text: str = "", excluded: bool = False) -> None:
    """Render a transparent button area with an optional SVG or text."""
    if svg_name:
        if svg_name.endswith("circle.svg") and excluded:
            svg_name = "resources/icons/table_cells/circle-off.svg"

        icon_size = int(min(rect.width(), rect.height()) - 6)
        icon_x = rect.left() + (rect.width() - icon_size) // 2
        icon_y = rect.top() + (rect.height() - icon_size) // 2

        pix = load_icon(svg_name, size=icon_size, color=self.text_color.name())
        if not pix.isNull():
            painter.drawPixmap(int(icon_x), int(icon_y), pix)
            return

    painter.save()
    if text:
        painter.setPen(self.text_color)
        painter.drawText(rect, Qt.AlignmentFlag.AlignCenter, text)
    else:
        painter.setPen(Qt.GlobalColor.red)
        painter.drawRect(rect.adjusted(4, 4, -4, -4))
    painter.restore()
