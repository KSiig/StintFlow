"""
Custom delegate for rendering status cells with icons.

Renders status column cells with appropriate icons and colored text.
"""

from PyQt6.QtWidgets import QStyledItemDelegate, QStyleOptionViewItem
from PyQt6.QtCore import Qt, QModelIndex, QRect
from PyQt6.QtGui import QPainter, QColor

from ui.utilities import load_icon
from core.utilities import resource_path


class StatusDelegate(QStyledItemDelegate):
    """
    Delegate for status column that renders text with status icons.
    
    Shows circle-check icon for "Completed" and hourglass for "Pending".
    """
    
    # Status configuration: maps status text to (icon_filename, color)
    STATUS_CONFIG = {
        "Completed": ("circle-check.svg", "#05fd7e"),
        "Pending": ("hourglass.svg", "#cf8b3c"),
    }
    
    def __init__(self, parent=None, icon_size: int = 16, icon_text_spacing: int = 6, left_margin: int = 8):
        """
        Initialize the delegate.
        
        Args:
            parent: Parent widget
            icon_size: Size of status icon in pixels (default: 16)
            icon_text_spacing: Pixels between icon and text (default: 6)
            left_margin: Pixels from left edge (default: 8)
        """
        super().__init__(parent)
        self.icon_size = icon_size
        self.icon_text_spacing = icon_text_spacing
        self.left_margin = left_margin
        self.default_color = QColor("#ffffff")  # Color for unknown statuses
    
    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        """
        Paint the status cell with icon and colored text.
        
        Args:
            painter: QPainter instance
            option: Style options for the item
            index: Model index of the cell
        """
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Get the status text
        text = index.data(Qt.ItemDataRole.DisplayRole)
        if not text:
            painter.restore()
            return
        
        # Get font
        font = index.data(Qt.ItemDataRole.FontRole)
        if font:
            painter.setFont(font)
        
        # Determine icon and color based on status
        status_config = self.STATUS_CONFIG.get(text)
        
        if status_config:
            icon_filename, color_hex = status_config
            icon_path = resource_path(f"resources/icons/table_cells/{icon_filename}")
            text_color = QColor(color_hex)
            
            # Load icon
            icon_pixmap = load_icon(icon_path, color=text_color.name())
        else:
            # Unknown status - use default color, no icon
            icon_pixmap = None
            text_color = self.default_color
        
        # Calculate positions
        x = option.rect.x() + self.left_margin
        icon_y = option.rect.y() + (option.rect.height() - self.icon_size) // 2
        
        # Draw icon if present
        if icon_pixmap:
            painter.drawPixmap(x, icon_y, self.icon_size, self.icon_size, icon_pixmap)
            x += self.icon_size + self.icon_text_spacing
        
        # Draw text with bounds checking
        painter.setPen(text_color)
        available_width = option.rect.width() - (x - option.rect.x())
        text_rect = QRect(x, option.rect.y(), max(0, available_width), option.rect.height())
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, text)
        
        painter.restore()
