from __future__ import annotations

from core.database import create_event, create_session, get_event, get_session
from core.errors import log, log_exception


def _clone_event(self) -> None:
    """Clone current event and create a practice session."""
    try:
        event_data = dict(self.event)
        if '_id' in event_data:
            del event_data['_id']
        event_data['name'] = event_data.get('name', 'Event') + " - Clone"

        result = create_event(event_data)
        if not result:
            log('ERROR', 'Failed to create cloned event', category='config_options', action='clone_event')
            return

        session_data = {
            "race_id": result.inserted_id,
            "name": "practice",
        }
        session_result = create_session(session_data)
        if not session_result:
            log('ERROR', 'Failed to create session for cloned event', category='config_options', action='clone_event')
            return

        new_event = get_event(str(result.inserted_id))
        new_session = get_session(str(session_result.inserted_id))

        if new_event and new_session:
            self.selection_model.set_event(str(new_event['_id']), new_event['name'])
            self.selection_model.set_session(str(new_session['_id']), new_session['name'])

        log('INFO', 'Event cloned successfully', category='config_options', action='clone_event')
    except Exception as e:
        log_exception(e, 'Failed to clone event', category='config_options', action='clone_event')
