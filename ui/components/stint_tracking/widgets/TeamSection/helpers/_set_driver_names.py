from __future__ import annotations

"""Helpers for managing driver name input widgets in TeamSection.

This module exports `_set_driver_names`, which rebuilds the driver input row
widgets from a list of driver names. It ensures existing widgets are cleared,
creates a new QLineEdit for each driver, and reattaches the change signal so the
containing TeamSection can track unsaved changes.

Expected API:
- `_set_driver_names(self, drivers: list[str]) -> None`
    - `drivers`: list of driver name strings (can be empty).
"""

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