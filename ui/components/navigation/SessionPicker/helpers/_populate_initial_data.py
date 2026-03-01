"""Populate combo boxes with initial data."""


def _populate_initial_data(self) -> None:
    """Load events and sessions, then apply selection from model."""
    self._load_events()

    if self.events.count() > 0:
        self._populate_sessions(self.events.currentData())

    self._apply_selection_from_model()
