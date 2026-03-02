"""Handle tracker stop event for ConfigView."""


def _on_tracker_stopped(self) -> None:
    """Stop active timers and refresh agents when tracking stops."""
    if getattr(self, "_startup_timer", None):
        self._startup_timer.stop()
        self._startup_timer = None
    if getattr(self, "_poll_timer", None):
        self._poll_timer.stop()
        self._poll_timer = None
    self.agent_overview._load_agents()
