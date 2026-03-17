from __future__ import annotations

from PyQt6.QtWidgets import QLineEdit
from ui.utilities import FONT, get_fonts
from ui.components.common import PopUp


def _add_row(self) -> None:
    """Add a new driver input row up to six entries."""
    if len(self.driver_inputs) < 6:
        line_edit = QLineEdit()
        line_edit.textEdited.connect(lambda _: self.changed.emit())
        line_edit.setFont(get_fonts(FONT.input_field))
        self.driver_box.addWidget(line_edit)
        self.driver_inputs.append(line_edit)
        self.changed.emit()
        return

    dialog = PopUp(
        title="Unable to add more rows",
        message="Maximum of 6 drivers allowed in a team.",
        buttons=["Ok"],
        type="warning",
        parent=self,
    )
    dialog.exec()
