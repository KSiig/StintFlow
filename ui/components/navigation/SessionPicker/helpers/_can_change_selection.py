"""Guard selection changes when another view has pending edits."""


def _can_change_selection(self) -> bool:
    """Return whether the current event/session selection may change."""
    if not self.selection_model:
        return True

    guard = getattr(self.selection_model, 'view_change_guard', None)
    if callable(guard):
        return bool(guard())

    return True