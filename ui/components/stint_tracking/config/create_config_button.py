"""
Create button for configuration options widget.

Returns a QPushButton with configurable width, icon, and styling.
"""

from PyQt6.QtWidgets import QPushButton
from PyQt6.QtGui import QIcon
from ui.utilities import load_icon
from .config_constants import ConfigLayout


def create_config_button(text: str, icon_path: str = None, icon_size: int = 16, 
                         icon_color: str = "#FFFFFF", width_type: str = 'third') -> QPushButton:
    """
    Create a button with optional icon.
    
    Args:
        text: Button text
        icon_path: Optional path to icon file (relative to resources/icons/)
        icon_size: Size of the icon in pixels (default: 16)
        icon_color: Optional color for the icon (e.g., '#05fd7e')
        width_type: Button width type - 'third', 'half', or 'full' (default: 'third')
        
    Returns:
        Configured QPushButton
    """
    # Determine button width based on type
    width_map = {
        'third': ConfigLayout.BTN_WIDTH_THIRD,
        'half': ConfigLayout.BTN_WIDTH_HALF,
        'full': ConfigLayout.BTN_WIDTH_FULL
    }
    button_width = width_map.get(width_type, ConfigLayout.BTN_WIDTH_THIRD)
    
    button = QPushButton(text)
    button.setFixedSize(button_width, ConfigLayout.BTN_HEIGHT)
    
    if icon_path:
        icon = load_icon(icon_path, size=icon_size, color=icon_color)
        if icon:
            button.setIcon(QIcon(icon))
    
    return button
