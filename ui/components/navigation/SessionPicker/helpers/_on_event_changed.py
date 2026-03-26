"""Handle event selection change."""


def _on_event_changed(self) -> None:
    """Update sessions list and selection model when event changes."""
    events_was_blocked = event_id = self.events.currentData()
    sessions_was_blocked = event_name = self.events.currentText()

    if not self._can_change_selection():
        self.events.blockSignals(True)
        self.sessions.blockSignals(True)
        try:
            self._apply_selection_from_model()
        finally:
            self.sessions.blockSignals(sessions_was_blocked)
            self.events.blockSignals(events_was_blocked)
        return

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
