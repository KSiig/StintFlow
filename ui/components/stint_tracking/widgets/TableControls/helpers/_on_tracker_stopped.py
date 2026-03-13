"""Update UI state when tracker stops."""

def _on_tracker_stopped(self) -> None:
  self._apply_tracking_state(False)
  self.agent_overview._load_agents()