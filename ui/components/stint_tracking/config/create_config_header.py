"""
Create header for configuration options widget.

Returns a horizontal layout with settings icon and title.
"""

from PyQt6.QtWidgets import QHBoxLayout, QLabel
from ui.utilities import get_fonts, FONT, load_icon
from .config_constants import ConfigLayout


def create_config_header() -> QHBoxLayout:
    """
    Create header with icon and title.
    
    Returns:
        QHBoxLayout containing icon and "Race Configuration" title
    """
    header_layout = QHBoxLayout()
    header_layout.setSpacing(ConfigLayout.HEADER_SPACING)
    header_layout.setContentsMargins(0, 0, 0, 0)
    
    # Settings icon
    icon_label = QLabel()
    settings_icon = load_icon('resources/icons/race_config/settings.svg', 
                              size=ConfigLayout.ICON_SIZE, color="#05fd7e")
    if settings_icon:
        icon_label.setPixmap(settings_icon)
    icon_label.setFixedSize(ConfigLayout.ICON_SIZE, ConfigLayout.ICON_SIZE)
    header_layout.addWidget(icon_label)
    
    # Title label
    title_label = QLabel("Race Configuration")
    title_label.setFont(get_fonts(FONT.header_input))
    header_layout.addWidget(title_label)
    header_layout.addStretch()
    
    return header_layout
