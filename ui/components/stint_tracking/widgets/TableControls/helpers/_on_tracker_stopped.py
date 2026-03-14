"""Update the UI and reload agents when the tracker stops.

This method updates the tracking state in the UI and reloads the agent overview
when the tracker process is stopped.
"""

def _on_tracker_stopped(self) -> None:
    self._apply_tracking_state(False)
    self.agent_overview._load_agents()