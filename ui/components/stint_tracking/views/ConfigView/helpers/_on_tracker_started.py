"""Handle tracker start event for ConfigView."""

from PyQt6.QtCore import QTimer


def _on_tracker_started(self) -> None:
    """Begin reloading agent list with initial burst polling."""
    self.agent_overview._load_agents()

    self._startup_count = 0
    self._startup_timer = QTimer(self)
    self._startup_timer.timeout.connect(self._startup_tick)
    self._startup_timer.start(500)
