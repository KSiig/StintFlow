"""Cleanup logic when the main window is closing."""

from PyQt6.QtWidgets import QMainWindow

from ui.components.stint_tracking import TrackerView


def closeEvent(self, event) -> None:
    """Ensure tracker shutdown runs when the app closes."""
    try:
        tracker_view = self.navigation_model.widgets.get(TrackerView)
        if tracker_view is not None and tracker_view.config_options is not None:
            tracker_view.config_options._shutdown_tracking()
    except Exception:
        pass

    QMainWindow.closeEvent(self, event)
