"""Respond to session selection changes."""

from core.errors import log
from ui.utilities.loading_queue import LoadingQueue

MESSAGE = "Loading strategies for new session..."


def _on_session_changed(self, session_id=None, session_name=None):
    """Reload strategies when the session changes and manage loading overlay."""
    log("DEBUG", "Session changed - reloading strategies", category="strategies_view", action="on_session_changed")

    LoadingQueue.push(MESSAGE)
    try:
        self._load_strategies()
    finally:
        LoadingQueue.pop(MESSAGE)
