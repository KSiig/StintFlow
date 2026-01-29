"""
Icon loading and colorization utilities.

Provides functions for loading SVG icons with color transformations and scaling.
"""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap, QPainter, QColor

from core.utilities import resource_path
from core.errors import log, log_exception


def load_icon(icon_path: str, size: int = 16, color: str = "#05fd7e") -> QPixmap:
    """
    Safely load an icon from a file path with error handling and colorization.
    
    Args:
        icon_path: Path to the icon file (relative to resources directory)
        size: Size to scale the icon to (height in pixels)
        color: Hex color code to apply to the icon (e.g., "#05fd7e")
        
    Returns:
        The loaded and colorized icon, or a null pixmap if loading fails
    """
    try:
        full_path = resource_path(icon_path)
        pixmap = QPixmap(full_path)
        
        if pixmap.isNull():
            log('WARNING', f'Icon file is empty or invalid: {icon_path}', category='ui', action='load_icon')
            return QPixmap()
        
        # Scale the icon
        scaled_pixmap = pixmap.scaledToHeight(size, Qt.TransformationMode.SmoothTransformation)
        
        # Colorize the icon
        colored_pixmap = QPixmap(scaled_pixmap.size())
        colored_pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(colored_pixmap)
        painter.drawPixmap(0, 0, scaled_pixmap)
        painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(colored_pixmap.rect(), QColor(color))
        painter.end()
        
        log('DEBUG', f'Icon loaded and colorized successfully: {icon_path}', category='ui', action='load_icon')
        return colored_pixmap
        
    except Exception as e:
        log_exception(e, f'Failed to load icon: {icon_path}', category='ui', action='load_icon')
        return QPixmap()
