"""Restart the application from the settings view."""

import sys
from pathlib import Path

from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QApplication

from core.errors import log, log_exception


def _restart_app(self) -> None:
    """Restart the application using the current interpreter."""
    try:
        executable = sys.executable
        script_path = Path(sys.argv[0]).resolve()
        if script_path.suffix.lower() == ".py":
            program = executable
            args = [str(script_path), *sys.argv[1:]]
        else:
            program = executable
            args = list(sys.argv[1:])
        started = QProcess.startDetached(program, args)
        if not started:
            log("ERROR", "Failed to start restart process", category="settings", action="restart")
            return
        log("INFO", "Restarting application from settings", category="settings", action="restart")
        QApplication.instance().quit()
    except Exception as exc:
        log_exception(exc, "Failed to restart application", category="settings", action="restart")
