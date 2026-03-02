from PyQt6.QtCore import QProcess
from PyQt6.QtWidgets import QApplication


def _restart_app(self) -> None:
    """Restart the application using the current interpreter."""
    try:
        program, args = self._get_restart_command()
        started = QProcess.startDetached(program, args)

        if not started:
            from core.errors import log

            log("ERROR", "Failed to start restart process", category="window_buttons", action="restart")
            return

        from core.errors import log

        log("INFO", "Restarting application", category="window_buttons", action="restart")
        QApplication.instance().quit()

    except Exception as exc:  # pragma: no cover - defensive logging
        from core.errors import log_exception

        log_exception(exc, "Failed to restart application", category="window_buttons", action="restart")
