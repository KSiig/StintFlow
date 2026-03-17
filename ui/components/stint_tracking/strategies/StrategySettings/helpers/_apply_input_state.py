from __future__ import annotations

"""Apply a captured input state back into the strategy settings UI.

This helper is used when a strategy settings view is refreshed or when the
user cancels edits. It updates the visible widgets, suppresses change
notifications while restoring, and (optionally) marks the restored state as
committed so that save/cancel buttons are hidden again.
"""


def _apply_input_state(self, input_state: dict[str, str | bool], persist_as_committed: bool = False) -> None:
    """Apply strategy setting values to the current input widgets."""
    self._is_restoring_input_state = True
    try:
        self.inputs['name'].setText(str(input_state.get('name', '')))
        self.inputs['mean_stint_time'].setText(str(input_state.get('mean_stint_time', '')))
        self.inputs['lock_completed_stints'].setChecked(bool(input_state.get('lock_completed_stints', False)))
    finally:
        self._is_restoring_input_state = False

    if persist_as_committed:
        self._committed_input_state = self._capture_input_state()
        self._has_unsaved_input_changes = False
        self.save_btn.hide()
        self.cancel_btn.hide()