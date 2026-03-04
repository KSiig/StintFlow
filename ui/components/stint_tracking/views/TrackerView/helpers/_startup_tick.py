"""Handle the startup polling burst ticks."""


def _startup_tick(self) -> None:
    """Poll agents during the startup burst, then transition to normal interval."""
    self._startup_count += 1
    self.agent_overview._load_agents()

    if self._startup_count >= 5:
        if getattr(self, "_startup_timer", None):
            self._startup_timer.stop()
            self._startup_timer = None
        self._start_polling_timer()
