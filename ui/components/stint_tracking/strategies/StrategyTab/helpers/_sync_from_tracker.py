"""Sync a strategy tab's data from the live tracker model."""

from __future__ import annotations

from core.errors import log

from ..StrategySyncWorker import StrategySyncWorker


def _sync_from_tracker(self) -> None:
    """Start a background sync from the live tracker into this strategy."""
    tracker_model = getattr(self, "tracker_table_model", None)
    if tracker_model is None:
        log(
            "WARNING",
            "Tracker model unavailable - cannot sync strategy",
            category="strategy_tab",
            action="sync_from_tracker",
        )
        return

    if self._sync_worker is not None and self._sync_worker.isRunning():
        log(
            "INFO",
            f"Sync already in progress for strategy {self.strategy_name}",
            category="strategy_tab",
            action="sync_from_tracker",
        )
        return

    tracker_rows, tracker_tires, _ = tracker_model.get_all_data()
    strategy_rows, strategy_tires, _ = self.table_model.get_all_data()

    self._sync_worker = StrategySyncWorker(
        strategy=self.strategy,
        strategy_name=self.strategy_name,
        tracker_rows=tracker_rows,
        tracker_tires=tracker_tires,
        strategy_rows=strategy_rows,
        strategy_tires=strategy_tires,
        mean_stint_time_seconds=int(self.table_model._mean_stint_time.total_seconds()),
    )
    self._sync_worker.sync_ready.connect(self._apply_sync_from_tracker_result)
    self._sync_worker.sync_failed.connect(self._handle_sync_from_tracker_failed)
    self._sync_worker.finished.connect(self._clear_sync_worker)
    self._sync_worker.finished.connect(self._sync_worker.deleteLater)
    self._sync_worker.start()