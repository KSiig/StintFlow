from __future__ import annotations

from core.database import update_event, update_session, update_team_drivers
from core.errors import log, log_exception


def _save_config(self) -> None:
    """Persist event, session, and driver changes."""
    try:
        update_event(
            str(self.selection_model.event_id),
            name=self.inputs['event_name'].text(),
            tires=self.inputs['tires'].text(),
            length=self.inputs['length'].text(),
            start_time=self.inputs['start_time'].text(),
        )

        update_session(
            str(self.selection_model.session_id),
            name=self.inputs['session_name'].text(),
        )

        drivers = [line_edit.text() for line_edit in self.driver_inputs]
        if self.team:
            update_team_drivers(str(self.team['_id']), drivers)
            self.drivers = drivers

        self.table_model.update_data()

        log('INFO', 'Configuration saved successfully', category='config_options', action='save_config')
    except Exception as e:
        log_exception(e, 'Failed to save configuration', category='config_options', action='save_config')
