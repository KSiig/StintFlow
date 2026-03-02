"""Locate parent view for positioning popups."""

from PyQt6.QtWidgets import QAbstractItemView


def _find_view(self, widget) -> QAbstractItemView | None:
    while widget:
        if isinstance(widget, QAbstractItemView):
            return widget
        widget = widget.parent()
    return None
