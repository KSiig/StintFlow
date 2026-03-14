"""Update the UI and load agents when the tracker starts.

This method updates the tracking state in the UI and reloads the agent overview
when the tracker process is started.
"""

def _on_tracker_started(self) -> None:
    self._apply_tracking_state(True)
    self.agent_overview._load_agents()