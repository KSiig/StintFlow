from __future__ import annotations

from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QIcon, QPainter
from PyQt6.QtWidgets import QStyle, QStyleOptionHeader


def paint_section(self, painter: QPainter, rect: QRect, logical_index: int) -> None:
    """Paint a header cell with configurable icon/text spacing."""
    painter.save()

    model = self.model()
    if not model:
        super(type(self), self).paintSection(painter, rect, logical_index)
        painter.restore()
        return

    text = model.headerData(logical_index, self.orientation(), Qt.ItemDataRole.DisplayRole)
    icon = model.headerData(logical_index, self.orientation(), Qt.ItemDataRole.DecorationRole)
    text_color = model.headerData(logical_index, self.orientation(), Qt.ItemDataRole.ForegroundRole)

    opt = QStyleOptionHeader()
    self.initStyleOption(opt)
    opt.rect = rect
    opt.section = logical_index
    opt.text = ""
    opt.icon = QIcon()
    self.style().drawControl(QStyle.ControlElement.CE_Header, opt, painter, self)

    x = rect.x() + self.left_padding
    y = rect.y()

    if icon and not icon.isNull():
        icon_y = y + (rect.height() - self.icon_size) // 2
        painter.drawPixmap(x, icon_y, self.icon_size, self.icon_size, icon)
        x += self.icon_size + self.icon_text_spacing

    if text:
        if self.font():
            painter.setFont(self.font())

        if text_color:
            painter.setPen(text_color)
        else:
            painter.setPen(opt.palette.color(opt.palette.ColorRole.WindowText))

        available_width = rect.width() - (x - rect.x())
        text_rect = QRect(x, y, max(0, available_width), rect.height())
        painter.drawText(
            text_rect,
            Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter,
            str(text),
        )

    painter.restore()
