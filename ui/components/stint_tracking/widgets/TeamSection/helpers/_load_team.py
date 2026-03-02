from __future__ import annotations

from PyQt6.QtWidgets import QLineEdit

from core.database import get_team
from ui.utilities import FONT, get_fonts

from ....config import ConfigLabels

def _load_team(self) -> None:
    """Load team from database and populate driver inputs."""
    self._clear_drivers()
    team = get_team()
    if team:
        self.drivers = team.get('drivers', [])
        for driver in self.drivers:
            line_edit = QLineEdit(driver)
            line_edit.setFont(get_fonts(FONT.input_field))
            line_edit.setReadOnly(True)
            self.driver_box.addWidget(line_edit)
            self.driver_inputs.append(line_edit)
