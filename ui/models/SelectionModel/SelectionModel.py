from PyQt6.QtCore import QObject, pyqtSignal

from .bounded_functions._set_event import _set_event
from .bounded_functions._set_session import _set_session


class SelectionModel(QObject):
    """Model for tracking the currently selected event and session."""

    eventChanged = pyqtSignal(object, object)
    sessionChanged = pyqtSignal(object, object)
    selectionChanged = pyqtSignal(object, object)

    _set_event = _set_event
    _set_session = _set_session

    def __init__(self):
        super().__init__()
        self._event_id = None
        self._session_id = None
        self._event_name = None
        self._session_name = None

    @property
    def event_id(self):
        return self._event_id

    @property
    def session_id(self):
        return self._session_id

    @property
    def event_name(self):
        return self._event_name

    @property
    def session_name(self):
        return self._session_name

    def set_event(self, event_id, event_name=""):
        self._set_event(event_id, event_name)

    def set_session(self, session_id, session_name=""):
        self._set_session(session_id, session_name)
