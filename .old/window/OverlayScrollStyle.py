from PyQt6.QtWidgets import QProxyStyle, QStyle, QStyleOptionSlider
from PyQt6.QtGui import QPainter, QColor
from PyQt6.QtCore import Qt

class OverlayScrollStyle(QProxyStyle):
    def drawControl(self, element, option, painter, widget=None):
        # Only paint the handle, skip the rest
        if element in (
            QStyle.ControlElement.CE_ScrollBarAddLine,
            QStyle.ControlElement.CE_ScrollBarSubLine,
            QStyle.ControlElement.CE_ScrollBarAddPage,
            QStyle.ControlElement.CE_ScrollBarSubPage,
            QStyle.ControlElement.CE_ScrollBarSlider,  # We'll paint this
        ):
            if element == QStyle.ControlElement.CE_ScrollBarSlider:
                # Paint the handle
                painter.save()
                r = option.rect
                color = QColor(100, 100, 100, 180)  # semi-transparent gray
                painter.setBrush(color)
                painter.setPen(Qt.PenStyle.NoPen)
                painter.drawRoundedRect(r, 5, 5)  # rounded handle
                painter.restore()
            # else: skip painting all other parts
        else:
            super().drawControl(element, option, painter, widget)

    def pixelMetric(self, metric, option=None, widget=None):
        if metric == QStyle.PixelMetric.PM_ScrollBarExtent:
            return 10  # thin handle
        return super().pixelMetric(metric, option, widget)
