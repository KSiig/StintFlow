from PyQt6.QtCore import QObject, pyqtSignal

class SelectionModel(QObject):
    eventChanged = pyqtSignal(object)
    sessionChanged = pyqtSignal(object)
    selectionChanged = pyqtSignal(object, object)

    def __init__(self):
        super().__init__()
        self._event_id = None
        self._session_id = None

    @property
    def event_id(self):
        return self._event_id

    @property
    def session_id(self):
        return self._session_id

    def set_event(self, event_id):
        if event_id != self._event_id:
            self._event_id = event_id
            self.eventChanged.emit(event_id)
            self.selectionChanged.emit(self._event_id, self._session_id)

    def set_session(self, session_id):
        if session_id != self._session_id:
            self._session_id = session_id
            self.sessionChanged.emit(session_id)
            self.selectionChanged.emit(self._event_id, self._session_id)
