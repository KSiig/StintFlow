"""Start or stop automatic strategy syncing when the toggle changes."""

from __future__ import annotations


def _handle_auto_sync_toggled(self, enabled: bool) -> None:
    """Update icon state and timer activity for the auto-sync toggle."""
    self._update_auto_sync_icon(enabled)

    if enabled:
        self.sync_requested.emit()
        self._auto_sync_timer.start(self._get_auto_sync_interval_seconds() * 1000)
        return

    self._auto_sync_timer.stop()