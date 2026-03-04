from __future__ import annotations


def _toggle_track(self) -> None:
    """Toggle stint tracking on/off."""
    if not self._tracking_active:
        self._start_process()
        if self._tracking_active:
            self.tracker_started.emit()
        return

    self._revert_tracking_state()
    if self.p:
        self.p.kill()
        self.p = None
    self.tracker_stopped.emit()
