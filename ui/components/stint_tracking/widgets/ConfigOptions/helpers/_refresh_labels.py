from __future__ import annotations

from core.database import get_event, get_session, get_sessions, get_team
from core.errors import log, log_exception


def _refresh_labels(self) -> None:
    """Reload event/session/team info into inputs."""
    try:
        self.event = get_event(self.selection_model.event_id)
        if not self.event:
            log('WARNING', 'No event found for current selection', category='config_options', action='refresh_labels')
            return

        self.session = get_session(self.selection_model.session_id)
        if not self.session:
            sessions = list(get_sessions(self.event['_id']))
            if sessions:
                self.session = sessions[-1]
                self.selection_model.set_session(str(self.session['_id']), self.session['name'])

        self.team = get_team()
        if self.team:
            self.drivers = self.team.get('drivers', [])
            for i, driver in enumerate(self.drivers):
                if i < len(self.driver_inputs):
                    self.driver_inputs[i].setText(driver)

        if self.event:
            self.inputs['event_name'].setText(self.event.get('name', ''))
            self.inputs['tires'].setText(str(self.event.get('tires', '')))
            self.inputs['length'].setText(self.event.get('length', ''))
            self.inputs['start_time'].setText(self.event.get('start_time', ''))

        if self.session:
            self.inputs['session_name'].setText(self.session.get('name', ''))
    except Exception as e:
        log_exception(e, 'Failed to refresh configuration labels', category='config_options', action='refresh_labels')
