"""Handle session selection change."""


def _on_session_changed(self) -> None:
    """Update selection model when session changes."""
    if self.selection_model:
        self.selection_model.set_session(
            self.sessions.currentData(),
            self.sessions.currentText(),
        )
