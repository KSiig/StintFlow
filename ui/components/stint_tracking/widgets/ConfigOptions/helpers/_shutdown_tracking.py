from __future__ import annotations

from PyQt6.QtCore import QProcess


def _shutdown_tracking(self) -> None:
    """Stop the tracker process and cleanup any registered agent."""
    was_tracking_active = bool(self._tracking_active)
    has_running_process = bool(
        self.p and self.p.state() == QProcess.ProcessState.Running
    )

    if not was_tracking_active and not has_running_process and not self.agent_name:
        return

    self._revert_tracking_state()

    if has_running_process:
        self.p.kill()
        self.p.waitForFinished()

    self.p = None

    if was_tracking_active:
        self.tracker_stopped.emit()