"""
Create driver names section for configuration options.

Returns a QFrame with driver input fields.
"""

from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLineEdit, QSizePolicy
from ui.utilities import get_fonts, FONT
from core.database import get_team
from .create_config_label import create_config_label
from .config_constants import ConfigLayout


def create_team_section() -> tuple[QFrame, list[QLineEdit], list[str]]:
    """
    Create the driver names configuration section.
    
    Returns:
        Tuple of:
        - QFrame containing driver input fields
        - List of QLineEdit widgets for each driver
        - List of driver names loaded from database
    """
    card = QFrame()
    card.setObjectName("DriverNames")
    card.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
    card.setContentsMargins(0, 0, 0, 0)
    
    title_label = create_config_label("Driver names")
    
    main_box = QVBoxLayout(card)
    main_box.setContentsMargins(0, 0, 0, 0)
    main_box.setSpacing(8)
    main_box.addWidget(title_label)
    
    driver_box = QVBoxLayout()
    driver_box.setSpacing(ConfigLayout.DRIVER_SPACING)
    main_box.addLayout(driver_box)
    
    # Load team and create driver inputs
    driver_inputs = []
    drivers = []
    
    team = get_team()
    if team:
        drivers = team.get('drivers', [])
        for driver in drivers:
            line_edit = QLineEdit(driver)
            line_edit.setFont(get_fonts(FONT.input_field))
            line_edit.setReadOnly(True)
            driver_box.addWidget(line_edit)
            driver_inputs.append(line_edit)
    
    return card, driver_inputs, drivers
