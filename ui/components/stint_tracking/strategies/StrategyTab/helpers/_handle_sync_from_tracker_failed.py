"""Handle background strategy sync failures."""

from __future__ import annotations

from core.errors import log


def _handle_sync_from_tracker_failed(self, strategy_name: str) -> None:
    """Log a background sync failure after the worker reports it."""
    log(
        "ERROR",
        f"Failed to sync strategy {strategy_name} from tracker",
        category="strategy_tab",
        action="sync_from_tracker",
    )