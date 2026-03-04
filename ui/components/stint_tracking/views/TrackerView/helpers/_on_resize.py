"""Constrain TableControls width to the visible right-column area."""

from __future__ import annotations

from PyQt6.QtGui import QResizeEvent
from PyQt6.QtWidgets import QWidget


def _on_resize(self, event: QResizeEvent) -> None:
    """Re-cap table_controls width on every window resize."""
    QWidget.resizeEvent(self, event)
    self._update_controls_width()
