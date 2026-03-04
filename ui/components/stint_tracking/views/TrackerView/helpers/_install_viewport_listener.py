"""Install a resize event filter on the scroll area viewport."""

from __future__ import annotations

from PyQt6.QtCore import QEvent, QObject
from PyQt6.QtWidgets import QScrollArea


class _ViewportResizeFilter(QObject):
    """Forwards viewport resize events to TrackerView._update_controls_width."""

    def __init__(self, tracker_view: QObject) -> None:
        super().__init__(tracker_view)
        self._tracker_view = tracker_view

    def eventFilter(self, obj: QObject, event: QEvent) -> bool:
        if event.type() == QEvent.Type.Resize:
            self._tracker_view._update_controls_width()
        return False  # never swallow the event


def _install_viewport_listener(self) -> None:
    """Attach the resize filter to the scroll area viewport.

    Called from showEvent so self.window() is already available.
    """
    if getattr(self, '_viewport_filter', None) is not None:
        return  # already installed

    win = self.window()
    scroll_area = getattr(win, 'central_scroll_area', None)
    if not isinstance(scroll_area, QScrollArea):
        return

    self._viewport_filter = _ViewportResizeFilter(self)
    scroll_area.viewport().installEventFilter(self._viewport_filter)
