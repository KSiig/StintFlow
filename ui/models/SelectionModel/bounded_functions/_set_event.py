def _set_event(self, event_id, event_name=""):
    """Set the currently selected event and emit signals when it changes."""
    if event_id != self._event_id:
        self._event_id = event_id
        self._event_name = event_name
        self.eventChanged.emit(event_id, event_name)
        self.selectionChanged.emit(self._event_id, self._session_id)
