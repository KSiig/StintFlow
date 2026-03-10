"""Clear the active strategy sync worker reference."""

from __future__ import annotations


def _clear_sync_worker(self) -> None:
    """Forget the current sync worker after it finishes."""
    self._sync_worker = None