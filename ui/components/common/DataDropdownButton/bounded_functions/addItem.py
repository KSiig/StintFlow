def addItem(self, text: str, userData: str = None) -> None:
      """Add a new item with optional user data."""
      self._items.append((text, userData))
      self._refresh_items(emit=False)

      if self._current_index == -1 and self._items:
          self.setCurrentIndex(0)