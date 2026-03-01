def findData(self, value) -> int:
    """Find index by user data value."""
    for index, (_, data) in enumerate(self._items):
        if data == value or str(data) == str(value):
            return index
    return -1