"""Apply event/session selection from the selection model."""


def _apply_selection_from_model(self) -> None:
    """Set combo boxes based on selection model values if available."""
    if not self.selection_model:
        return

    event_id = self.selection_model.event_id
    session_id = self.selection_model.session_id

    if event_id:
        event_index = self.events.findData(str(event_id))
        if event_index >= 0:
            self.events.setCurrentIndex(event_index)

    if session_id:
        session_index = self.sessions.findData(str(session_id))
        if session_index >= 0:
            self.sessions.setCurrentIndex(session_index)
