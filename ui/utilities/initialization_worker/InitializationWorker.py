"""Background worker used during application startup."""

from datetime import timedelta

from PyQt6.QtCore import QThread, pyqtSignal

from core.database import get_events, get_sessions
from core.database.connection import test_connection
from core.errors import log_exception
from ui.models.table_loader import load_table_data


class InitializationWorker(QThread):
    """Thread that loads data needed to populate the initial views."""

    status = pyqtSignal(str)
    connectionFailed = pyqtSignal()
    finished = pyqtSignal(list, list, timedelta, list, list)

    def __init__(self, selection_model):
        super().__init__()
        self.selection_model = selection_model

    def run(self) -> None:
        try:
            self.status.emit("Connecting to database...")
            if not test_connection():
                self.status.emit("Unable to connect to MongoDB")
                self.connectionFailed.emit()
                return

            self.status.emit("Loading navigation data...")
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

            self.status.emit("Loading table data...")
            data, tires, mean = load_table_data(self.selection_model)
            self.status.emit("Initialization complete")
            self.finished.emit(data, tires, mean, events, sessions)
        except Exception as e:
            log_exception(
                e,
                "Error during background initialization",
                category="ui",
                action="init_worker",
            )
            self.finished.emit([], [], timedelta(0), [], [])
