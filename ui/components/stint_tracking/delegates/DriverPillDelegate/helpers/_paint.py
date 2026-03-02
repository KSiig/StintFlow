"""Paint driver names with pill background."""

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPen
from PyQt6.QtWidgets import QStyleOptionViewItem, QStyledItemDelegate

from ui.components.stint_tracking.delegates.delegate_utils import paint_model_background


def _paint(self, painter, option: QStyleOptionViewItem, index):
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

    text_rect = painter.fontMetrics().boundingRect(text)
    pill_width = min(text_rect.width() + (self.padding_horizontal * 2), option.rect.width() - (self.left_margin * 2))
    pill_height = text_rect.height() + (self.padding_vertical * 2)

    pill_rect = QRect(
        option.rect.x() + self.left_margin,
        option.rect.y() + (option.rect.height() - pill_height) // 2,
        pill_width,
        pill_height,
    )

    painter.setPen(Qt.PenStyle.NoPen)
    painter.setBrush(self.background_color)
    painter.drawRoundedRect(pill_rect, self.border_radius, self.border_radius)

    painter.setPen(QPen(self.text_color))
    painter.drawText(pill_rect, Qt.AlignmentFlag.AlignCenter, text)

    painter.restore()
