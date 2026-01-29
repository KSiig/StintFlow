"""
Selection model for tracking event and session selection state.

Emits signals when event or session changes to notify UI components.
"""

from PyQt6.QtCore import QObject, pyqtSignal


class SelectionModel(QObject):
    """
    Model for tracking the currently selected event and session.
    
    Signals:
        eventChanged: Emitted when event selection changes (event_id, event_name)
        sessionChanged: Emitted when session selection changes (session_id, session_name)
        selectionChanged: Emitted when either event or session changes (event_id, session_id)
    """
    
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
        """Get the currently selected event ID."""
        return self._event_id

    @property
    def session_id(self):
        """Get the currently selected session ID."""
        return self._session_id

    @property
    def event_name(self):
        """Get the currently selected event name."""
        return self._event_name

    @property
    def session_name(self):
        """Get the currently selected session name."""
        return self._session_name

    def set_event(self, event_id, event_name=""):
        """
        Set the currently selected event.
        
        Args:
            event_id: MongoDB ObjectId of the event
            event_name: Display name of the event (optional)
        """
        if event_id != self._event_id:
            self._event_id = event_id
            self._event_name = event_name
            self.eventChanged.emit(event_id, event_name)
            self.selectionChanged.emit(self._event_id, self._session_id)

    def set_session(self, session_id, session_name=""):
        """
        Set the currently selected session.
        
        Args:
            session_id: MongoDB ObjectId of the session
            session_name: Display name of the session (optional)
        """
        if session_id != self._session_id:
            self._session_id = session_id
            self._session_name = session_name
            self.sessionChanged.emit(session_id, session_name)
            self.selectionChanged.emit(self._event_id, self._session_id)
