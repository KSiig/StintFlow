from __future__ import annotations

from ui.components.common import PopUp


def _remove_row(self) -> None:
    """Remove the last driver row while keeping at least one."""
    if len(self.driver_inputs) > 1:
        line_edit = self.driver_inputs.pop()
        self.driver_box.removeWidget(line_edit)
        line_edit.deleteLater()
        self.changed.emit()
        return

    dialog = PopUp(
        title="Can't remove more rows",
        message="You need at least one driver in a team.",
        buttons=["Ok"],
        type="warning",
        parent=self,
    )
    dialog.exec()
