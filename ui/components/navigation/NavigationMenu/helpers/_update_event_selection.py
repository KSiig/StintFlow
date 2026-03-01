"""Reload session picker when event or session selection changes."""


def _update_event_selection(self) -> None:
    """Delegate reload to the session picker."""
    self.session_picker.reload()
