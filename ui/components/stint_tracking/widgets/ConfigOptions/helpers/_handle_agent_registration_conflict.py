from __future__ import annotations

from ui.components.common import PopUp


def _handle_agent_registration_conflict(self) -> None:
    """Warn about agent name conflicts and stop tracking."""
    dialog = PopUp(
        title="Agent name conflict",
        message="Agent name conflict detected! Please choose a different name in settings.",
        buttons=["Ok"],
        type="error",
        parent=self,
    )
    dialog.exec()
    self._toggle_track()
