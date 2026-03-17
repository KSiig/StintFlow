from __future__ import annotations

"""Capture strategy settings input widget values for undo/cancel handling.

This module provides a single helper used by StrategySettings to take a
snapshot of the current input widget contents so the UI can be restored if the
user cancels edits.
"""


def _capture_input_state(self) -> dict[str, str | bool]:
    """Capture the current strategy settings input state."""
    return {
        'name': self.inputs['name'].text(),
        'mean_stint_time': self.inputs['mean_stint_time'].text(),
        'lock_completed_stints': bool(self.inputs['lock_completed_stints'].isChecked()),
    }