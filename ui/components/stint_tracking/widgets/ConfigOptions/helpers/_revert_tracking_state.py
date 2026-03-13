from __future__ import annotations

from core.database import delete_agent


def _revert_tracking_state(self) -> None:
    """Restore UI to pre-tracking state and cleanup agent registration."""
    self.lbl_info.hide()
    if self.agent_name:
        delete_agent(self.agent_name)
        self.agent_name = None
    self._tracking_active = False
