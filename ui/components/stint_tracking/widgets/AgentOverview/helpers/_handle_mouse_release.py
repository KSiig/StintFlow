"""Mouse handler for AgentOverview to trigger the popup."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame


def _handle_mouse_release(self, event) -> None:
    """Open or close the popup in response to a click."""
    QFrame.mouseReleaseEvent(self, event)
    if event.button() != Qt.MouseButton.LeftButton:
        return
    if self._popup.isVisible():
        self._popup.hide()
        return
    self._open_popup()
