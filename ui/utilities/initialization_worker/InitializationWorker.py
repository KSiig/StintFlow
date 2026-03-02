"""Background worker used during application startup."""

from datetime import timedelta

from PyQt6.QtCore import QThread, pyqtSignal

from core.database import get_events, get_sessions
from core.database.connection import test_connection
from core.errors import log_exception
from ui.models.table_loader import load_table_data
from ui.utilities.loading_queue import LoadingQueue

_MSG_CONNECT = "Connecting to database..."
_MSG_NAV = "Loading navigation data..."
_MSG_TABLE = "Loading table data..."


class InitializationWorker(QThread):
    """Thread that loads data needed to populate the initial views."""

    connectionFailed = pyqtSignal()
    finished = pyqtSignal(list, list, timedelta, list, list)

    def __init__(self, selection_model):
        super().__init__()
        self.selection_model = selection_model

    def run(self) -> None:
        try:
            LoadingQueue.push(_MSG_CONNECT)
            try:
                connected = test_connection()
            finally:
                LoadingQueue.pop(_MSG_CONNECT)

            if not connected:
                self.connectionFailed.emit()
                return

            LoadingQueue.push(_MSG_NAV)
            try:
                try:
                    events = list(get_events(sort_by=None))
                except Exception:
                    events = []
                sessions = []
                if events:
                    try:
                        sessions = list(get_sessions(str(events[0].get("_id")), sort_by=None))
                    except Exception:
                        sessions = []
            finally:
                LoadingQueue.pop(_MSG_NAV)

            LoadingQueue.push(_MSG_TABLE)
            try:
                data, tires, mean = load_table_data(self.selection_model)
                self.finished.emit(data, tires, mean, events, sessions)
            finally:
                LoadingQueue.pop(_MSG_TABLE)

        except Exception as e:
            log_exception(
                e,
                "Error during background initialization",
                category="ui",
                action="init_worker",
            )
            self.finished.emit([], [], timedelta(0), [], [])
