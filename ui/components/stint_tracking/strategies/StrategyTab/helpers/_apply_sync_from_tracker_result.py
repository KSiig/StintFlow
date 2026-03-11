"""Apply completed tracker sync results on the GUI thread."""

from __future__ import annotations

from datetime import timedelta

from core.errors import log


def _apply_sync_from_tracker_result(self, result: dict) -> None:
    """Apply worker-produced strategy data back into the table and UI."""
    mean_stint_time_seconds = int(result.get("mean_stint_time_seconds", 0))

    self.table_model.update_data(
        data=result.get("merged_rows", []),
        tires=result.get("merged_tires", []),
        mean_stint_time=timedelta(seconds=mean_stint_time_seconds),
    )
    self.table_model._recalculate_tires_left()

    self.strategy["model_data"] = result.get("model_data", {})
    self.strategy["mean_stint_time_seconds"] = mean_stint_time_seconds
    self.strategy["last_sync"] = result.get("last_sync")

    self.stint_table.refresh_table(skip_model_update=True)
    if not hasattr(self, "actions_delegate") or self.actions_delegate is None:
        self._setup_strategy_delegates()
    self._open_persistent_editors()

    log(
        "INFO",
        f"Synced {int(result.get('completed_count', 0))} tracker stints into strategy {self.strategy_name}",
        category="strategy_tab",
        action="sync_from_tracker",
    )

    self.sync_completed.emit(self.strategy)