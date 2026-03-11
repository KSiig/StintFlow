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

        if self.sync_widget is not None:
            current_index = self.stacked_widget.currentIndex()
            current_widget = self.stacked_widget.widget(current_index) if current_index >= 0 else None
            self.sync_widget._set_strategy(getattr(current_widget, "strategy", None) if current_widget is not None else None)

        log("INFO", "Removed strategy tab after deletion", category="strategies_view", action="remove_tab")
    else:
        log("WARNING", "Attempted to remove non-existent tab", category="strategies_view", action="remove_tab")
