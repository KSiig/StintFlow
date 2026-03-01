def _on_value_changed(self, value: str) -> None:
    index = -1
    for i, (label, _) in enumerate(self._items):
        if label == value:
            index = i
            break

    self._current_index = index

    if not self._signals_blocked:
        self.currentIndexChanged.emit(self._current_index)