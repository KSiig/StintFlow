"""Install viewport listener and apply initial width when TrackerView is shown."""

from __future__ import annotations

from PyQt6.QtGui import QShowEvent
from PyQt6.QtWidgets import QWidget


def _on_show(self, event: QShowEvent) -> None:
    """Hook first show to install the viewport resize listener."""
    QWidget.showEvent(self, event)
    self._install_viewport_listener()
    self._update_controls_width()
