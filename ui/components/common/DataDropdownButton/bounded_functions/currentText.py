def currentText(self) -> str:
    """Return label text for the current item."""
    if self._current_index < 0:
        return ""
    return self._items[self._current_index][0]