"""Switch stacked widget page when tab changes."""


def _on_tab_changed(self, index: int) -> None:
    """Handle tab change by switching stacked widget page."""
    self.stacked_widget.setCurrentIndex(index)

    if self.sync_widget is None:
        return

    current_tab = self.stacked_widget.widget(index) if index >= 0 else None
    strategy = getattr(current_tab, "strategy", None) if current_tab is not None else None
    self.sync_widget._set_strategy(strategy)
