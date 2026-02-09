"""
Create configuration row with label and input field.

Returns a QFrame containing a labeled input field.
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLineEdit, QSizePolicy
from PyQt6.QtCore import Qt
from ui.utilities import get_fonts, FONT
from .create_config_label import create_config_label
from .config_constants import ConfigLayout


def create_config_row(title: str) -> tuple[QFrame, QLineEdit]:
    """
    Create a configuration row with label and input field.
    
    Args:
        title: Display title for the field
        
    Returns:
        Tuple of (QFrame containing the row, QLineEdit input field reference)
    """
    card = QFrame()
    card.setObjectName("Setting")
    card.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum)
    card.setContentsMargins(0, 0, 0, 0)
    
    main_box = QVBoxLayout(card)
    main_box.setContentsMargins(0, 0, 0, 0)
    main_box.setSpacing(ConfigLayout.ROW_SPACING)
    
    # Create label
    title_label = create_config_label(title)
    
    # Create input
    input_field = QLineEdit()
    input_field.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
    input_field.setFixedHeight(ConfigLayout.INPUT_HEIGHT)
    input_field.setFont(get_fonts(FONT.input_field))
    input_field.setReadOnly(True)
    input_field.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    input_field.setContentsMargins(0, 0, 0, 0)
    
    # Add to layout
    main_box.addWidget(title_label)
    main_box.addWidget(input_field, stretch=1)
    
    return card, input_field
