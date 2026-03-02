from __future__ import annotations

from PyQt6.QtWidgets import QLineEdit


def _toggle_edit(self) -> None:
    """Toggle between view and edit modes."""
    if self.save_btn.isVisible():
        self.save_btn.hide()
        self.edit_btn.show()
        self.team_section._set_active(False)
        for child in self.findChildren(QLineEdit):
            child.setReadOnly(True)
            child.setProperty('editable', False)
            child.style().unpolish(child)
            child.style().polish(child)
        return

    self.edit_btn.hide()
    self.save_btn.show()
    self.team_section._set_active(True)
    for child in self.findChildren(QLineEdit):
        child.setReadOnly(False)
        child.setProperty('editable', True)
        child.style().unpolish(child)
        child.style().polish(child)
