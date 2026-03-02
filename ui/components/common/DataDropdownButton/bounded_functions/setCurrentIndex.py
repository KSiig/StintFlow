def setCurrentIndex(self, index: int) -> None:
    """Set current selection by index."""
    if index < 0 or index >= len(self._items):
        self._current_index = -1
        self.dropdown.set_value("")
    else:
        self._current_index = index
        self.dropdown.set_value(self._items[index][0])

    if not self._signals_blocked:
        self.currentIndexChanged.emit(self._current_index)