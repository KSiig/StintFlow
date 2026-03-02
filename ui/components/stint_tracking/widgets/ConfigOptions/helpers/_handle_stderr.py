from __future__ import annotations

from core.errors import log


def _handle_stderr(self) -> None:
    """Process stderr output from stint_tracker."""
    if not self.p:
        return

    data = self.p.readAllStandardError()
    stderr = bytes(data).decode("utf8")
    self._handle_output(stderr)
    log('ERROR', f'Stint tracker stderr: {stderr}', category='config_options', action='handle_stderr')
