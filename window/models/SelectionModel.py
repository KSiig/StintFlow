from PyQt6.QtCore import QObject, pyqtSignal

class SelectionModel(QObject):
    eventChanged = pyqtSignal(object, object)
    sessionChanged = pyqtSignal(object, object)
    selectionChanged = pyqtSignal(object, object)

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

    def set_event(self, event_id, event_name = ""):
        if event_id != self._event_id:
            self._event_id = event_id
            self._event_name = event_name
            self.eventChanged.emit(event_id, event_name)
            self.selectionChanged.emit(self._event_id, self._session_id)

    def set_session(self, session_id, session_name = ""):
        if session_id != self._session_id:
            self._session_id = session_id
            self._session_name = session_name
            self.sessionChanged.emit(session_id, session_name)
            self.selectionChanged.emit(self._event_id, self._session_id)
