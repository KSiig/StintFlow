"""
Create label for configuration input field.

Returns a QLabel with title text and minimal spacing.
"""

from PyQt6.QtWidgets import QLabel, QSizePolicy
from PyQt6.QtCore import Qt
from ui.utilities import get_fonts, FONT


def create_config_label(title: str) -> QLabel:
    """
    Create a title label for a configuration field.
    
    Args:
        title: Title text
        
    Returns:
        Configured title label with minimal vertical spacing
    """
    title_label = QLabel(title)
    title_label.setObjectName("SettingTitle")
    title_label.setFont(get_fonts(FONT.input_lbl))
    title_label.setContentsMargins(0, 0, 0, 0)
    title_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    title_label.setAlignment(Qt.AlignmentFlag.AlignTop)
    
    # Remove font's extra vertical spacing by setting max height to exact text height
    font_metrics = title_label.fontMetrics()
    title_label.setMaximumHeight(font_metrics.height())
    
    return title_label
