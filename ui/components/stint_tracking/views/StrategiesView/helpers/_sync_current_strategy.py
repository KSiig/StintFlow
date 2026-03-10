"""Dispatch strategy sync requests from the StrategiesView header control."""

from __future__ import annotations

from core.errors import log


def _sync_current_strategy(self) -> None:
    """Sync the currently selected strategy tab from the live tracker model."""
    if self.stacked_widget is None:
        return

    current_index = self.stacked_widget.currentIndex()
    current_tab = self.stacked_widget.widget(current_index) if current_index >= 0 else None

    if current_tab is None or not hasattr(current_tab, "_sync_from_tracker"):
        log(
            "WARNING",
            "No active strategy tab available for sync",
            category="strategies_view",
            action="sync_current_strategy",
        )
        return

    current_tab._sync_from_tracker()