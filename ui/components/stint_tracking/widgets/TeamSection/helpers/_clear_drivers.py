from __future__ import annotations


def _clear_drivers(self) -> None:
    """Remove all driver input widgets."""
    for line_edit in self.driver_inputs:
        self.driver_box.removeWidget(line_edit)
        line_edit.deleteLater()
    self.driver_inputs = []
    self.drivers = []
