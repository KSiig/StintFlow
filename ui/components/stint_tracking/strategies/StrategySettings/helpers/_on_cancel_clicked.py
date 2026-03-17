from __future__ import annotations


def _on_cancel_clicked(self) -> None:
    """Restore the last committed strategy settings values."""
    if self._committed_input_state is None:
        return

    self._apply_input_state(self._committed_input_state)
    self._has_unsaved_input_changes = False
    self.save_btn.hide()
    self.cancel_btn.hide()