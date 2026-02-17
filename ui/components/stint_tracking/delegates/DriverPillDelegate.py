"""
Custom delegate for rendering driver names as pills.

Renders driver column cells with rounded background (pill shape).
"""

from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem
from PyQt6.QtCore import Qt, QModelIndex, QRect
from PyQt6.QtGui import QPainter, QColor, QPen

from .delegate_utils import paint_model_background


class DriverPillDelegate(QStyledItemDelegate):
    """
    Delegate for driver column that renders text in a pill-shaped background.
    
    Creates rounded rectangle backgrounds for driver names with custom styling.
    """
    
    def __init__(self, parent=None, background_color: str = "#0e4c35", text_color: str = "#ffffff"):
        """
        Initialize the delegate.
        
        Args:
            parent: Parent widget
            background_color: Hex color for pill background (default: dark green)
            text_color: Hex color for text (default: white)
        """
        super().__init__(parent)
        self.background_color = QColor(background_color)
        self.text_color = QColor(text_color)
        self.border_radius = 12
        self.padding_horizontal = 12
        self.padding_vertical = 4
        self.left_margin = 8  # Space from left edge
    
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        """
        Paint the driver cell with pill-shaped background.
        
        Args:
            painter: QPainter instance
            option: Style options for the item
            index: Model index of the cell
        """
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Paint any model-provided background (e.g. excluded-row tint)
        paint_model_background(painter, option, index)
        
        # Get the text
        text = index.data(Qt.ItemDataRole.DisplayRole)
        if not text:
            painter.restore()
            return
        
        # Get font
        font = index.data(Qt.ItemDataRole.FontRole)
        if font:
            painter.setFont(font)
        
        # Calculate text size
        text_rect = painter.fontMetrics().boundingRect(text)
        
        # Calculate pill dimensions with bounds checking
        pill_width = text_rect.width() + (self.padding_horizontal * 2)
        pill_height = text_rect.height() + (self.padding_vertical * 2)
        
        # Ensure pill doesn't exceed cell width
        max_pill_width = option.rect.width() - (self.left_margin * 2)
        pill_width = min(pill_width, max_pill_width)
        
        pill_rect = QRect(
            option.rect.x() + self.left_margin,
            option.rect.y() + (option.rect.height() - pill_height) // 2,
            pill_width,
            pill_height
        )
        
        # Draw rounded rectangle background
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(self.background_color)
        painter.drawRoundedRect(pill_rect, self.border_radius, self.border_radius)
        
        # Draw text
        painter.setPen(QPen(self.text_color))
        painter.drawText(pill_rect, Qt.AlignmentFlag.AlignCenter, text)
        
        painter.restore()
