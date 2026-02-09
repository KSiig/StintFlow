"""
Custom horizontal header view with icon spacing control.

Subclasses QHeaderView to provide custom spacing between icons and text.
"""

from PyQt6.QtWidgets import QHeaderView, QStyleOptionHeader, QStyle
from PyQt6.QtCore import Qt, QRect
from PyQt6.QtGui import QPainter, QIcon


class SpacedHeaderView(QHeaderView):
    """
    Horizontal header view with custom icon-to-text spacing.
    
    Overrides painting to add configurable spacing between icon and text.
    """
    
    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None, icon_text_spacing: int = 8, left_padding: int = 8):
        """
        Initialize the header view.
        
        Args:
            orientation: Header orientation (horizontal/vertical)
            parent: Parent widget
            icon_text_spacing: Pixels between icon and text (default: 8)
            left_padding: Pixels from left edge (default: 8)
        """
        super().__init__(orientation, parent)
        self.icon_text_spacing = icon_text_spacing
        self.left_padding = left_padding
        self.icon_size = 16  # Icon dimensions in pixels
    
    def paintSection(self, painter: QPainter, rect: QRect, logicalIndex: int) -> None:
        """
        Paint a header section with custom icon-text spacing.
        
        Args:
            painter: QPainter instance
            rect: Section rectangle
            logicalIndex: Logical index of the section
        """
        painter.save()
        
        # Get the model
        model = self.model()
        if not model:
            super().paintSection(painter, rect, logicalIndex)
            painter.restore()
            return
        
        # Get header data
        text = model.headerData(logicalIndex, self.orientation(), Qt.ItemDataRole.DisplayRole)
        icon = model.headerData(logicalIndex, self.orientation(), Qt.ItemDataRole.DecorationRole)
        text_color = model.headerData(logicalIndex, self.orientation(), Qt.ItemDataRole.ForegroundRole)
        
        # Draw background (use default style)
        opt = QStyleOptionHeader()
        self.initStyleOption(opt)
        opt.rect = rect
        opt.section = logicalIndex
        opt.text = ""  # We'll draw text ourselves
        opt.icon = QIcon()  # Empty icon - we'll draw it ourselves
        self.style().drawControl(QStyle.ControlElement.CE_Header, opt, painter, self)
        
        # Calculate positions
        x = rect.x() + self.left_padding
        y = rect.y()
        
        # Draw icon if present
        if icon and not icon.isNull():
            icon_y = y + (rect.height() - self.icon_size) // 2
            painter.drawPixmap(x, icon_y, self.icon_size, self.icon_size, icon)
            x += self.icon_size + self.icon_text_spacing
        
        # Draw text
        if text:
            if self.font():
                painter.setFont(self.font())
            
            # Use custom color if provided, otherwise use default
            if text_color:
                painter.setPen(text_color)
            else:
                painter.setPen(opt.palette.color(opt.palette.ColorRole.WindowText))
            
            # Calculate text rect with bounds checking
            available_width = rect.width() - (x - rect.x())
            text_rect = QRect(x, y, max(0, available_width), rect.height())
            painter.drawText(text_rect, Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter, str(text))
        
        painter.restore()
