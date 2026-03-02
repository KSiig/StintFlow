from __future__ import annotations


def _handle_stdout(self) -> None:
    """Process stdout output from stint_tracker."""
    if not self.p:
        return

    data = self.p.readAllStandardOutput()
    stdout = bytes(data).decode("utf8")
    self._handle_output(stdout)
