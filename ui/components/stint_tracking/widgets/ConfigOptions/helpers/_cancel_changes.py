from __future__ import annotations


def _cancel_changes(self) -> None:
    """Restore the most recently committed configuration values."""
    if self._committed_form_state is None:
        return

    self._apply_form_state(self._committed_form_state)
    self._has_unsaved_form_changes = False
    self.save_btn.hide()
    self.cancel_btn.hide()