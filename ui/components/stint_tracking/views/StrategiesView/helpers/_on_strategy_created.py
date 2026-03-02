"""Handle strategy creation events."""

from core.errors import log, log_exception


def _on_strategy_created(self, strategy: dict) -> None:
    """Handle strategy creation from StrategyTab."""
    try:
        tab = self._create_strategy_tab(strategy)
        self._add_tab(tab, strategy["name"])

        log("INFO", f"Added tab for new strategy: {strategy['name']}", category="strategies_view", action="on_strategy_created")

        self.strategy_created.emit(strategy)
    except Exception as exc:
        log_exception(exc, "Failed to create strategy tab", category="strategies_view", action="on_strategy_created")
