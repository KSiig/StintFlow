"""Background worker for syncing strategy data from the live tracker."""

from __future__ import annotations

import copy
from datetime import datetime, timezone

from PyQt6.QtCore import QThread, pyqtSignal

from core.database import update_strategy
from core.errors import log_exception
from ui.models.stint_helpers import sanitize_stints
from ui.models.table_constants import ColumnIndex
from ui.models.table_processors import recalculate_pending_tires_changed


class StrategySyncWorker(QThread):
    """Sync completed tracker rows into a strategy off the GUI thread."""

    sync_ready = pyqtSignal(dict)
    sync_failed = pyqtSignal(str)

    def __init__(
        self,
        strategy: dict,
        strategy_name: str,
        tracker_rows: list[list],
        tracker_tires: list[dict],
        strategy_rows: list[list],
        strategy_tires: list[dict],
        mean_stint_time_seconds: int = None,
    ) -> None:
        super().__init__()
        self.strategy = copy.deepcopy(strategy)
        self.strategy_name = strategy_name
        self.tracker_rows = copy.deepcopy(tracker_rows)
        self.tracker_tires = copy.deepcopy(tracker_tires)
        self.strategy_rows = copy.deepcopy(strategy_rows)
        self.strategy_tires = copy.deepcopy(strategy_tires)
        self.mean_stint_time_seconds = mean_stint_time_seconds

    def run(self) -> None:
        """Build merged strategy data and persist it in the background."""
        try:
            completed_rows: list[list] = []
            completed_tires: list[dict] = []

            for row_index, row in enumerate(self.tracker_rows):
                if "Completed" not in str(row[ColumnIndex.STATUS]):
                    break

                completed_rows.append(copy.deepcopy(row))
                completed_tires.append(
                    copy.deepcopy(self.tracker_tires[row_index])
                    if row_index < len(self.tracker_tires)
                    else {}
                )

            pending_rows: list[list] = []
            pending_tires: list[dict] = []

            for row_index, row in enumerate(self.strategy_rows):
                if "Completed" in str(row[ColumnIndex.STATUS]):
                    continue

                pending_rows.append(copy.deepcopy(row))
                pending_tires.append(
                    copy.deepcopy(self.strategy_tires[row_index])
                    if row_index < len(self.strategy_tires)
                    else {}
                )

            merged_rows = completed_rows + pending_rows
            merged_tires = completed_tires + pending_tires

            recalculate_pending_tires_changed(
                data=merged_rows,
                tires=merged_tires,
                completed_count=len(completed_rows),
            )

            sanitized = sanitize_stints(merged_rows, merged_tires)
            last_sync = datetime.now(timezone.utc).isoformat()

            model_data = self.strategy.setdefault("model_data", {})
            model_data["rows"] = sanitized.get("rows", [])
            model_data["tires"] = sanitized.get("tires", [])
            self.strategy["model_data"] = model_data
            self.strategy["mean_stint_time_seconds"] = self.mean_stint_time_seconds
            self.strategy["last_sync"] = last_sync

            update_strategy(strategy=self.strategy)

            self.sync_ready.emit(
                {
                    "completed_count": len(completed_rows),
                    "merged_rows": merged_rows,
                    "merged_tires": merged_tires,
                    "mean_stint_time_seconds": self.mean_stint_time_seconds,
                    "model_data": model_data,
                    "last_sync": last_sync,
                }
            )
        except Exception as exc:
            log_exception(
                exc,
                f"Failed to sync strategy {self.strategy_name} from tracker",
                category="strategy_tab",
                action="sync_from_tracker",
            )
            self.sync_failed.emit(self.strategy_name)