"""Create a strategy tab widget."""

from ui.components.stint_tracking.strategies import StrategyTab


def _create_strategy_tab(self, strategy: dict):
    """Create a tab widget for an existing strategy."""
    tab = StrategyTab(strategy=strategy, table_model=self.table_model, selection_model=self.selection_model)
    tab.name_changed.connect(lambda new_name, t=tab: self._update_tab_label(t, new_name))
    tab.deleted.connect(lambda sid, t=tab: self._remove_tab(t))
    tab.sync_completed.connect(
        lambda synced_strategy, t=tab: self.sync_widget._set_strategy(synced_strategy)
        if self.sync_widget is not None and self.stacked_widget.currentWidget() is t
        else None
    )
    return tab
