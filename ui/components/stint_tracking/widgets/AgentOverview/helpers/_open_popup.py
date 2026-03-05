"""Helper to refresh data and display the popup."""

from __future__ import annotations


def _open_popup(self) -> None:
    """Refresh agents and show the floating list."""
    self._load_agents()
    width = max(self.width(), 320)
    self._popup.setFixedWidth(width)
    self._popup.adjustSize()
    target = self.mapToGlobal(self.rect().bottomLeft())
    target.setY(target.y() + 4)
    self._popup.move(target)
    self._popup.show()
