"""
Background worker used during application startup to perform expensive
initialization tasks without blocking the main GUI thread.

Currently the only work performed is loading the initial stint table data, but
this may expand in the future.
"""

from datetime import timedelta
from PyQt6.QtCore import QThread, pyqtSignal
from core.errors import log_exception

from core.database.connection import test_connection
from core.database import get_events, get_sessions
from ui.models.table_loader import load_table_data


class InitializationWorker(QThread):
    """Thread that loads data needed to populate the initial views.

    Signals:
        status (str): emitted with a short status message while work progresses.
        connectionFailed: emitted if the database connection cannot be established.
        finished (list, list, timedelta, list, list): emitted when work is
            complete with the loaded table rows, tire metadata, mean stint time,
            a list of events, and a list of sessions for the first event.
    """
    status = pyqtSignal(str)
    connectionFailed = pyqtSignal()
    finished = pyqtSignal(list, list, timedelta, list, list)

    def __init__(self, selection_model):
        super().__init__()
        self.selection_model = selection_model

    def run(self) -> None:
        try:
            # first test database connectivity
            self.status.emit('Connecting to database...')
            if not test_connection():
                self.status.emit('Unable to connect to MongoDB')
                self.connectionFailed.emit()
                return

            # load navigation data while we're here
            self.status.emit('Loading navigation data...')
            try:
                events = list(get_events(sort_by=None))
            except Exception:
                events = []
            sessions = []
            if events:
                # get sessions for the first event only
                try:
                    sessions = list(get_sessions(str(events[0].get('_id')), sort_by=None))
                except Exception:
                    sessions = []

            # proceed with normal table loading
            self.status.emit('Loading table data...')
            data, tires, mean = load_table_data(self.selection_model)
            self.status.emit('Initialization complete')
            self.finished.emit(data, tires, mean, events, sessions)
        except Exception as e:
            log_exception(e, 'Error during background initialization',
                          category='ui', action='init_worker')
            # still emit something so UI can continue
            self.finished.emit([], [], timedelta(0), [], [])
