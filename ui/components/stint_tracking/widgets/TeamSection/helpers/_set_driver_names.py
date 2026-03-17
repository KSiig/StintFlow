from __future__ import annotations

from PyQt6.QtWidgets import QLineEdit

from ui.utilities import FONT, get_fonts


def _set_driver_names(self, drivers: list[str]) -> None:
    """Replace driver inputs with the provided driver names."""
    self._clear_drivers()
    self.drivers = list(drivers)

    for driver in self.drivers:
        line_edit = QLineEdit(driver)
        line_edit.textEdited.connect(lambda _: self.changed.emit())
        line_edit.setFont(get_fonts(FONT.input_field))
        self.driver_box.addWidget(line_edit)
        self.driver_inputs.append(line_edit)