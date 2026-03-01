def clear(self) -> None:
    """Clear all items and reset selection."""
    self._items = []
    self._current_index = -1
    self.dropdown.set_items([])
    self.dropdown.set_value("")