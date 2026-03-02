"""Remove a specific tab and its widget."""

from PyQt6.QtWidgets import QWidget

from core.errors import log


def _remove_tab(self, widget: QWidget) -> None:
    """Remove the given widget/tab from the interface."""
    index = self.stacked_widget.indexOf(widget)
    if index != -1:
        self.tab_bar.removeTab(index)
        self.stacked_widget.removeWidget(widget)
        widget.deleteLater()
        log("INFO", "Removed strategy tab after deletion", category="strategies_view", action="remove_tab")
    else:
        log("WARNING", "Attempted to remove non-existent tab", category="strategies_view", action="remove_tab")
