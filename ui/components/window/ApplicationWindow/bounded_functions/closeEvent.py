"""Cleanup logic when the main window is closing."""

from PyQt6.QtWidgets import QMainWindow

from ui.components.stint_tracking import TrackerView
from core.errors import log_exception
from PyQt6.QtGui import QCloseEvent


def closeEvent(self, event: QCloseEvent) -> None:
    """Ensure tracker shutdown runs when the app closes."""
    try:
        tracker_view = self.navigation_model.widgets.get(TrackerView)
        if tracker_view is not None and tracker_view.config_options is not None:
            tracker_view.config_options._shutdown_tracking()
    except Exception as exc:
        log_exception(exc, 'DEBUG', f'Exception during tracker shutdown',
            category='application_window', action='close_event')

    QMainWindow.closeEvent(self, event)
