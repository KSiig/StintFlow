from __future__ import annotations

"""Capture the current ConfigOptions form state for undo/restore purposes.

This module exports `_capture_form_state`, which takes a snapshot of all
ConfigOptions input widgets (event/session fields, tire/config values, and
driver names). The snapshot is used by the cancel flow to restore the UI to a
previously committed state.
"""


def _capture_form_state(self) -> dict[str, str | list[str]]:
    """Capture the current configuration form values."""
    return {
        'event_name': self.inputs['event_name'].text(),
        'session_name': self.inputs['session_name'].text(),
        'tires': self.inputs['tires'].text(),
        'length': self.inputs['length'].text(),
        'start_time': self.inputs['start_time'].text(),
        'tires_remaining_at_green_flag': self.inputs['tires_remaining_at_green_flag'].text(),
        'drivers': [line_edit.text() for line_edit in self.driver_inputs],
    }