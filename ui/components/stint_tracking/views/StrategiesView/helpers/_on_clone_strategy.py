"""Clone the currently selected strategy tab."""

import copy

from bson import ObjectId

from core.database import create_strategy
from core.errors import log, log_exception
from ui.components.stint_tracking.strategies import StrategyTab


def _on_clone_strategy(self):
    """Clone the selected strategy tab and insert it as a new strategy."""
    try:
        if not self.selection_model.session_id:
            log("WARNING", "No session selected - cannot clone strategy", category="strategies_view", action="clone_strategy")
            return

        idx = self.tab_bar.currentIndex()
        if idx < 0 or idx >= self.stacked_widget.count():
            log("WARNING", "No strategy tab is currently selected", category="strategies_view", action="clone_strategy")
            return

        widget = self.stacked_widget.widget(idx)
        if not isinstance(widget, StrategyTab):
            log("WARNING", "Selected tab cannot be cloned (not a StrategyTab)", category="strategies_view", action="clone_strategy")
            return

        original = widget.strategy
        if not original:
            log("WARNING", "Selected strategy has no data to clone", category="strategies_view", action="clone_strategy")
            return

        new_strategy = copy.deepcopy(original)
        new_strategy["name"] = f"{original.get('name','Unnamed Strategy')} - Clone"
        new_strategy.pop("_id", None)
        new_strategy["session_id"] = ObjectId(self.selection_model.session_id)

        strategy_id = create_strategy(new_strategy)
        new_strategy["_id"] = strategy_id

        log("INFO", f"Cloned strategy \"{original.get('name')}\"", category="strategies_view", action="clone_strategy")

        self._on_strategy_created(new_strategy)

        return new_strategy
    except Exception as exc:
        log_exception(exc, "Failed to clone strategy", category="strategies_view", action="clone_strategy")
