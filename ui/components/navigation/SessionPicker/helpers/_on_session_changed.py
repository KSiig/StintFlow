"""Handle session selection change."""


def _on_session_changed(self) -> None:
    """Update selection model when session changes."""
    if not self._can_change_selection():
        self.events.blockSignals(True)
        self.sessions.blockSignals(True)
        try:
            self._apply_selection_from_model()
        finally:
            self.sessions.blockSignals(False)
            self.events.blockSignals(False)
        return

    if self.selection_model:
        self.selection_model.set_session(
            self.sessions.currentData(),
            self.sessions.currentText(),
        )
