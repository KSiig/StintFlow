"""Switch stacked widget page when tab changes."""


def _on_tab_changed(self, index: int) -> None:
    """Handle tab change by switching stacked widget page."""
    self.stacked_widget.setCurrentIndex(index)
