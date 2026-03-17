from __future__ import annotations

"""Apply captured configuration form state to ConfigOptions widgets.

This module defines the `_apply_form_state` helper used by ConfigOptions to
restore a previously captured snapshot of the input fields. It updates all
visible input widgets (including driver rows) while suppressing "dirty"
change notifications, and it can optionally mark the restored state as
committed (hiding save/cancel buttons).

Expected API:
- `_apply_form_state(self, form_state, persist_as_committed=False)`
    - `form_state`: dict with values for keys like 'event_name', 'session_name',
      'tires', 'length', 'start_time', 'tires_remaining_at_green_flag',
      and 'drivers'.
    - `persist_as_committed`: if True, the restored state becomes the new
      baseline and unsaved-change tracking is reset.
"""


def _apply_form_state(self, form_state: dict[str, str | list[str]], persist_as_committed: bool = False) -> None:
    """Apply configuration values to the current form widgets."""
    self._is_restoring_form_state = True
    try:
        self.inputs['event_name'].setText(str(form_state.get('event_name', '')))
        self.inputs['session_name'].setText(str(form_state.get('session_name', '')))
        self.inputs['tires'].setText(str(form_state.get('tires', '')))
        self.inputs['length'].setText(str(form_state.get('length', '')))
        self.inputs['start_time'].setText(str(form_state.get('start_time', '')))
        self.inputs['tires_remaining_at_green_flag'].setText(str(form_state.get('tires_remaining_at_green_flag', '')))

        driver_names = [str(driver) for driver in form_state.get('drivers', [])]
        self.team_section._set_driver_names(driver_names)
        self.driver_inputs = self.team_section.get_driver_inputs()
        self.drivers = list(driver_names)
    finally:
        self._is_restoring_form_state = False

    if persist_as_committed:
        self._committed_form_state = self._capture_form_state()
        self._has_unsaved_form_changes = False
        self.save_btn.hide()
        self.cancel_btn.hide()