"""Handle event selection change."""


def _on_event_changed(self) -> None:
    """Update sessions list and selection model when event changes."""
    event_id = self.events.currentData()
    event_name = self.events.currentText()

    if self.selection_model:
        self.selection_model.set_event(event_id, event_name)

    self._populate_sessions(event_id)

    if self.sessions.count() > 0 and self.selection_model:
        self.selection_model.set_session(
            self.sessions.currentData(),
            self.sessions.currentText(),
        )
    elif self.selection_model:
        self.selection_model.set_session(None)
