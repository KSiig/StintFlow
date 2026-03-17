from __future__ import annotations

"""Handle keyboard save shortcuts for the StrategySettings panel."""


def _handle_save_shortcut(self) -> None:
    """Trigger a save when Ctrl+S is pressed and the inputs have unsaved changes."""
    if not self._has_unsaved_input_changes:
        return

    self._on_save_clicked()