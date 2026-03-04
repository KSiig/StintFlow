"""Recalculate and apply the maximum width for the right column."""

from __future__ import annotations

from PyQt6.QtWidgets import QScrollArea


def _update_controls_width(self) -> None:
    """Cap right_column_container to the visible available width.

    Accounts for the left column being visible or hidden, and the spacing
    between the two columns. StintTable and TableControls inside it will
    fill the container naturally.
    """
    if self.right_column_container is None:
        return

    win = self.window()
    scroll_area = getattr(win, 'central_scroll_area', None)
    if not isinstance(scroll_area, QScrollArea):
        return

    available = scroll_area.viewport().width()

    left = getattr(self, 'left_column_container', None)
    if left is not None and not left.isHidden():
        available -= left.width() + self.SPACING

    self.right_column_container.setMaximumWidth(max(available, 0))
