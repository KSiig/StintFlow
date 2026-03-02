"""Remove all strategy tabs."""

from core.errors import log


def _clear_tabs(self) -> None:
    """Remove all tabs and stacked widgets."""
    while self.tab_bar.count() > 0:
        self.tab_bar.removeTab(0)

    while self.stacked_widget.count() > 0:
        widget = self.stacked_widget.widget(0)
        self.stacked_widget.removeWidget(widget)
        widget.deleteLater()

    log("DEBUG", "Cleared strategy tabs", category="strategies_view", action="clear_tabs")
