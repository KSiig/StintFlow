from __future__ import annotations

from PyQt6.QtWidgets import QLineEdit

from ui.components.common import PopUp
from ui.utilities import FONT, get_fonts
from ....config import fetch_team_from_lmu


def _fetch_drivers(self) -> None:
    """Fetch driver names from LMU and populate inputs."""
    team = fetch_team_from_lmu()
    if team:
        self._clear_drivers()
        self.drivers = team
        for driver in self.drivers:
            line_edit = QLineEdit(driver)
            line_edit.setFont(get_fonts(FONT.input_field))
            line_edit.setReadOnly(True)
            self.driver_box.addWidget(line_edit)
            self.driver_inputs.append(line_edit)
        return

    dialog = PopUp(
        title="No team data found",
        message="Unable to fetch drivers because no team data is available.",
        buttons=["Ok"],
        type="error",
        parent=self,
    )
    dialog.exec()
