from __future__ import annotations


def _capture_input_state(self) -> dict[str, str | bool]:
    """Capture the current strategy settings input state."""
    return {
        'name': self.inputs['name'].text(),
        'mean_stint_time': self.inputs['mean_stint_time'].text(),
        'lock_completed_stints': bool(self.inputs['lock_completed_stints'].isChecked()),
    }