from __future__ import annotations

from core.errors import log


def _handle_process_error(self, error) -> None:
    """Handle process-level errors and revert UI state."""
    if not self.p:
        return

    error_message = self.p.errorString()
    log('ERROR', f'Stint tracker process error: {error_message}', category='config_options', action='process_error')
    if self._tracking_active:
        self._revert_tracking_state()
        self.p = None
