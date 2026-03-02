from __future__ import annotations

from datetime import datetime

from core.database import create_session
from core.errors import log, log_exception


def _create_session(self) -> None:
    """Create a new session for the current event."""
    try:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_name = "Practice - " + now

        session_data = {
            "race_id": self.event['_id'],
            "name": session_name,
        }

        result = create_session(session_data)
        if not result:
            log('ERROR', 'Failed to create new session', category='config_options', action='create_session')
            return

        self.selection_model.set_session(str(result.inserted_id), session_name)
        log('INFO', f'Created new session: {session_name}', category='config_options', action='create_session')
    except Exception as e:
        log_exception(e, 'Failed to create session', category='config_options', action='create_session')
