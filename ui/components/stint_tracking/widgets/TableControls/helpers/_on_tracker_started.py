"""Update UI state when tracker starts."""

def _on_tracker_started(self) -> None:
  self._apply_tracking_state(True)
  self.agent_overview._load_agents()