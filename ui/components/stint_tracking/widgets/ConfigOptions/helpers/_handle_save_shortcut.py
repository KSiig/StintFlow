from __future__ import annotations

"""Handle keyboard save shortcuts for the ConfigOptions panel."""


def _handle_save_shortcut(self) -> None:
    """Trigger a save when Ctrl+S is pressed and the form has unsaved changes."""
    if not self._has_unsaved_form_changes:
        return

    self._save_config()