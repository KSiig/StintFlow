from __future__ import annotations

from core.errors import log


def _handle_process_finished(self, exit_code, exit_status) -> None:
    """Handle process exit to keep UI state in sync."""
    if not self._tracking_active:
        return

    log('WARNING', f'Stint tracker exited: code={exit_code}, status={exit_status}', category='config_options', action='process_finished')
    self._revert_tracking_state()
    self.p = None
