from __future__ import annotations

from core.database import delete_agent


def _revert_tracking_state(self) -> None:
    """Restore UI to pre-tracking state and cleanup agent registration."""
    self.stop_btn.hide()
    self.start_btn.show()
    self.lbl_info.hide()
    delete_agent(self.agent_name)
