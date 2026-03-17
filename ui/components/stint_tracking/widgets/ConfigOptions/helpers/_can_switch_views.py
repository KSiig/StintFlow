from __future__ import annotations

from ui.components.common import PopUp


def _can_switch_views(self) -> bool:
    """Block navigation while configuration edits are pending."""
    if not self._has_unsaved_form_changes:
        return True

    dialog = PopUp(
        title="Unsaved changes",
        message="Please save or cancel your configuration changes before switching views.",
        buttons=["Ok"],
        type="warning",
        parent=self,
    )
    dialog.exec()
    return False