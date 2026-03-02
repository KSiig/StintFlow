"""Paint status cells with icon and colored text."""

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QColor

from ui.components.stint_tracking.delegates.delegate_utils import paint_model_background
from ui.utilities.load_icon import load_icon
from core.utilities import resource_path


def _paint(self, painter, option, index):
    painter.save()
    painter.setRenderHint(painter.RenderHint.Antialiasing)

    paint_model_background(painter, option, index)

    text = index.data(Qt.ItemDataRole.DisplayRole)
    if not text:
        painter.restore()
        return

    font = index.data(Qt.ItemDataRole.FontRole)
    if font:
        painter.setFont(font)

    status_config = self.STATUS_CONFIG.get(text)
    if status_config:
        icon_filename, color_hex = status_config
        icon_path = resource_path(f"resources/icons/table_cells/{icon_filename}")
        text_color = QColor(color_hex)
        icon_pixmap = load_icon(icon_path, color=text_color.name(), size=self.icon_size)
    else:
        icon_pixmap = None
        text_color = self.default_color

    x = option.rect.x() + self.left_margin
    icon_y = option.rect.y() + (option.rect.height() - self.icon_size) // 2

    if icon_pixmap:
        painter.drawPixmap(x, icon_y, self.icon_size, self.icon_size, icon_pixmap)
        x += self.icon_size + self.icon_text_spacing

    painter.setPen(text_color)
    available_width = option.rect.width() - (x - option.rect.x())
    text_rect = QRect(x, option.rect.y(), max(0, available_width), option.rect.height())
    painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)

    painter.restore()
