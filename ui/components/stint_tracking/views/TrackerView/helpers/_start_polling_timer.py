"""Start the regular agent polling timer."""

from PyQt6.QtCore import QTimer

from core.utilities import load_user_settings


def _start_polling_timer(self) -> None:
    """Create and start the regular interval polling timer."""
    settings = load_user_settings()
    interval = settings.get("agent_poll_interval", 5) if isinstance(settings, dict) else 5
    try:
        interval = int(interval)
    except Exception:
        interval = 5

    self._poll_timer = QTimer(self)
    self._poll_timer.timeout.connect(self.agent_overview._load_agents)
    self._poll_timer.start(interval * 1000)
