def currentData(self):
    """Return user data for the current item."""
    if self._current_index < 0:
        return None
    return self._items[self._current_index][1]