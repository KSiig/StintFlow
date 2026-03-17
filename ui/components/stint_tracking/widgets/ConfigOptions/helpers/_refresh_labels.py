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
        tires_remaining = ''
        if self.session:
            tires_remaining = self.session.get('tires_remaining_at_green_flag')
            if tires_remaining is None and self.event:
                tires_remaining = self.event.get('tires', '') or ''

        form_state = {
            'event_name': self.event.get('name', '') if self.event else '',
            'session_name': self.session.get('name', '') if self.session else '',
            'tires': str(self.event.get('tires', '')) if self.event else '',
            'length': self.event.get('length', '') if self.event else '',
            'start_time': self.event.get('start_time', '') if self.event else '',
            'tires_remaining_at_green_flag': str(tires_remaining or ''),
            'drivers': self.team.get('drivers', []) if self.team else [],
        }
        self._apply_form_state(form_state, persist_as_committed=True)
    except Exception as e:
        log_exception(e, 'Failed to refresh configuration labels', category='config_options', action='refresh_labels')
