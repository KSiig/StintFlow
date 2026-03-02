"""Create a new strategy and add it as a tab."""

from bson import ObjectId

from core.database import create_strategy
from core.errors import log, log_exception
from ui.models.stint_helpers import sanitize_stints


def _on_create_strategy(self, name: str = None):
    """Handle strategy creation."""
    try:
        strategy_name = name if name else f"Strategy {self.tab_bar.count() + 1}"

        row_data, tire_data, mean_stint_time = self.table_model.get_all_data()
        sanitized_data = sanitize_stints(row_data, tire_data)

        if not row_data:
            log("WARNING", "No stint data to create strategy", category="strategies_view", action="create_strategy")
            return

        if not self.selection_model.session_id:
            log("WARNING", "No session selected", category="strategies_view", action="create_strategy")
            return

        strategy = {
            "session_id": ObjectId(self.selection_model.session_id),
            "name": strategy_name,
            "model_data": sanitized_data,
            "mean_stint_time_seconds": int(mean_stint_time.total_seconds()) if mean_stint_time else 0,
        }

        strategy_id = create_strategy(strategy)
        strategy["_id"] = strategy_id

        log("INFO", f"Strategy created: {strategy_name}", category="strategies_view", action="create_strategy")

        tab = self._create_strategy_tab(strategy)
        self._add_tab(tab, strategy_name)

        self.strategy_created.emit(strategy)

        return strategy
    except Exception as exc:
        log_exception(exc, "Failed to create strategy", category="strategies_view", action="create_strategy")
