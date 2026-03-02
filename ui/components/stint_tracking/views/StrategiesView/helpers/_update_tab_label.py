"""Update tab label text for a widget."""

from PyQt6.QtWidgets import QWidget

from core.errors import log


def _update_tab_label(self, widget: QWidget, new_label: str) -> None:
    """Update the tab bar text for the given widget."""
    index = self.stacked_widget.indexOf(widget)
    if index != -1:
        log("INFO", f"Updating tab label at index {index} to \"{new_label}\"", category="strategies_view", action="update_tab_label")
        self.tab_bar.setTabText(index, new_label)
        self.tab_bar.update()
        self.tab_bar.repaint()
    else:
        log("WARNING", "Attempted to update label for non-existent tab", category="strategies_view", action="update_tab_label")
