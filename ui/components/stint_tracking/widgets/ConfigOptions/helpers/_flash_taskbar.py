from __future__ import annotations

from PyQt6.QtWidgets import QApplication


def _flash_taskbar(self) -> None:
    """Request taskbar attention using QApplication.alert."""
    window = self.window()
    if window:
        QApplication.alert(window, 0)
