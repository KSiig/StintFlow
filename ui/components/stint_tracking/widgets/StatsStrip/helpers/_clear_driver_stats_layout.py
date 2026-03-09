"""Clear driver stat card widgets from a layout."""

from PyQt6.QtWidgets import QLayout


def _clear_driver_stats_layout(layout: QLayout) -> None:
    """Delete all widgets currently attached to the driver stats layout."""
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        child_layout = item.layout()

        if widget is not None:
            widget.deleteLater()
            continue

        if child_layout is not None:
            _clear_driver_stats_layout(child_layout)