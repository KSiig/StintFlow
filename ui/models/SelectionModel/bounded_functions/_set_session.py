def _set_session(self, session_id, session_name=""):
    """Set the currently selected session and emit signals when it changes."""
    if session_id != self._session_id:
        self._session_id = session_id
        self._session_name = session_name
        self.sessionChanged.emit(session_id, session_name)
        self.selectionChanged.emit(self._event_id, self._session_id)
