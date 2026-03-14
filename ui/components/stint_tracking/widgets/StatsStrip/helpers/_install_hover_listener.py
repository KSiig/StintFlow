"""Install hover listeners for StatsStrip scrollbar visibility."""

from __future__ import annotations

from PyQt6.QtCore import QEvent, QObject, QTimer


class _HoverFilter(QObject):
    """Toggle the horizontal scrollbar when the strip is hovered."""

    def __init__(self, stats_strip: QObject) -> None:
        super().__init__(stats_strip)
        self._stats_strip = stats_strip

    def eventFilter(self, _obj: QObject, event: QEvent) -> bool:
        if event.type() in {QEvent.Type.Enter, QEvent.Type.HoverEnter}:
            self._stats_strip._set_scrollbar_visibility(True)
        elif event.type() in {QEvent.Type.Leave, QEvent.Type.HoverLeave}:
            QTimer.singleShot(0, self._stats_strip._sync_scrollbar_visibility)

        return False


def _install_hover_listener(self) -> None:
    """Attach hover listeners to keep the scrollbar hidden until hovered."""
    if getattr(self, '_hover_filter', None) is not None:
        return

    self._hover_filter = _HoverFilter(self)

    widgets = [self._frame]
    if self.scroll_area:
        widgets.append(self.scroll_area.viewport())
        widgets.append(self.scroll_area.horizontalScrollBar())

    for widget in widgets:
        widget.installEventFilter(self._hover_filter)