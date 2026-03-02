"""Respond to session selection changes."""

from PyQt6.QtWidgets import QApplication

from core.errors import log


def _on_session_changed(self, session_id=None, session_name=None):
    """Reload strategies when the session changes and manage loading overlay."""
    app_window = self.window() or (QApplication.instance().activeWindow() if QApplication.instance() else None)
    log("DEBUG", "Session changed - reloading strategies", category="strategies_view", action="on_session_changed")

    if app_window and hasattr(app_window, "show_loading"):
        app_window.show_loading("Loading strategies for new session...")

    try:
        self._load_strategies()
    finally:
        if app_window and hasattr(app_window, "hide_loading"):
            app_window.hide_loading()
