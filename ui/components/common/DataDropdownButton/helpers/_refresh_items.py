def _refresh_items(self, emit: bool = True) -> None:
    # optionally sort the internal tuple list before extracting labels
    if self._sort_items:
        self._items.sort(key=lambda tup: str(tup[0]).lower())
    labels = [label for label, _ in self._items]
    self.dropdown.set_items(labels)

    if self._current_index >= len(self._items):
        self._current_index = -1
        self.dropdown.set_value("")

    if emit and not self._signals_blocked:
        self.currentIndexChanged.emit(self._current_index)