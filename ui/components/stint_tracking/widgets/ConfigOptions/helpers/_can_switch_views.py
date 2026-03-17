"""Helper utilities for ConfigOptions view switching.

This module provides logic used by the ConfigOptions workflow to determine
whether the user can navigate away from the current view when configuration
edits are pending.

The primary helper in this module, ``_can_switch_views``, is invoked before
switching views to enforce that changes are either saved or explicitly canceled.
If unsaved changes exist, it displays a ``PopUp`` warning dialog and blocks
navigation until the user resolves the pending edits.

The module is used by the ConfigOptions widget(s) as part of the view
switching / navigation guard logic.
"""

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