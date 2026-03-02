from __future__ import annotations


def _strategy_updated(self, updated_strategy: dict) -> None:
    """Handle updates from StrategySettings."""
    self.strategy = updated_strategy
    self.name_changed.emit(self.strategy.get('name', 'Unnamed Strategy'))
    self._load_strategy_data()
    self.table_model._recalculate_tires_left()
