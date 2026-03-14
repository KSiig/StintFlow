"""Sync scrollbar visibility with hover state."""

from PyQt6.QtCore import Qt


def _sync_scrollbar_visibility(self) -> None:
    """Update scrollbar visibility after hover transitions settle."""
    if self.scroll_area is None or self._frame is None:
        return

    is_hovered = any(
        widget is not None and widget.underMouse()
        for widget in (
            self._frame,
            self.scroll_area.viewport(),
            self.scroll_area.horizontalScrollBar(),
        )
    )
    self._set_scrollbar_visibility(is_hovered)
