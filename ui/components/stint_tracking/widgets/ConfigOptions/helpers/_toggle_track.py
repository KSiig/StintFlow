from __future__ import annotations


def _toggle_track(self) -> None:
    """Toggle stint tracking on/off."""
    if self.stop_btn.isHidden():
        self.start_btn.hide()
        self.stop_btn.show()
        self._start_process()
        self.tracker_started.emit()
        return

    self._revert_tracking_state()
    self._tracking_active = False
    if self.p:
        self.p.kill()
        self.p = None
    self.tracker_stopped.emit()
