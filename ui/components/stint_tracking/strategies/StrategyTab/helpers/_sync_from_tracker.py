"""Sync a strategy tab's data from the live tracker model."""

from __future__ import annotations

import copy

from datetime import datetime, timezone

from core.database import update_strategy
from core.errors import log, log_exception
from ui.models.stint_helpers import sanitize_stints
from ui.models.table_constants import ColumnIndex
from ui.models.table_processors import recalculate_pending_tires_changed


def _sync_from_tracker(self) -> None:
    """Copy tracker completed rows into the strategy and realign pending tire changes."""
    try:
        tracker_model = getattr(self, "tracker_table_model", None)
        if tracker_model is None:
            log(
                "WARNING",
                "Tracker model unavailable - cannot sync strategy",
                category="strategy_tab",
                action="sync_from_tracker",
            )
            return

        tracker_rows, tracker_tires, _ = tracker_model.get_all_data()
        strategy_rows, strategy_tires, _ = self.table_model.get_all_data()

        completed_rows: list[list] = []
        completed_tires: list[dict] = []

        for row_index, row in enumerate(tracker_rows):
            if "Completed" not in str(row[ColumnIndex.STATUS]):
                break

            completed_rows.append(copy.deepcopy(row))
            completed_tires.append(
                copy.deepcopy(tracker_tires[row_index])
                if row_index < len(tracker_tires)
                else {}
            )

        pending_rows: list[list] = []
        pending_tires: list[dict] = []

        for row_index, row in enumerate(strategy_rows):
            if "Completed" in str(row[ColumnIndex.STATUS]):
                continue

            pending_rows.append(copy.deepcopy(row))
            pending_tires.append(
                copy.deepcopy(strategy_tires[row_index])
                if row_index < len(strategy_tires)
                else {}
            )

        merged_rows = completed_rows + pending_rows
        merged_tires = completed_tires + pending_tires

        recalculate_pending_tires_changed(
            data=merged_rows,
            tires=merged_tires,
            completed_count=len(completed_rows),
        )

        self.table_model.update_data(
            data=merged_rows,
            tires=merged_tires,
            mean_stint_time=self.table_model._mean_stint_time,
        )
        self.table_model._recalculate_tires_left()

        row_data, tire_data, _ = self.table_model.get_all_data()
        sanitized = sanitize_stints(row_data, tire_data)

        model_data = self.strategy.setdefault("model_data", {})
        model_data["rows"] = sanitized.get("rows", [])
        model_data["tires"] = sanitized.get("tires", [])
        self.strategy["model_data"] = model_data
        self.strategy["mean_stint_time_seconds"] = int(self.table_model._mean_stint_time.total_seconds())
        self.strategy["last_sync"] = datetime.now(timezone.utc).isoformat()

        update_strategy(strategy=self.strategy)

        self.stint_table.refresh_table(skip_model_update=True)
        self._setup_strategy_delegates()
        self._open_persistent_editors()

        log(
            "INFO",
            f"Synced {len(completed_rows)} tracker stints into strategy {self.strategy_name}",
            category="strategy_tab",
            action="sync_from_tracker",
        )
    except Exception as exc:
        log_exception(
            exc,
            f"Failed to sync strategy {self.strategy_name} from tracker",
            category="strategy_tab",
            action="sync_from_tracker",
        )