from __future__ import annotations

from PyQt6.QtWidgets import QLineEdit


def _toggle_edit(self) -> None:
    """Toggle between view and edit modes."""
    if self.save_btn.isVisible():
        self.save_btn.hide()
        return

    self.save_btn.show()
