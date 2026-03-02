from PyQt6.QtCore import QModelIndex


def columnCount(self, parent: QModelIndex = None) -> int:  # type: ignore[override]
    """Return number of columns in model."""
    if parent is None:
        parent = QModelIndex()
    return len(self._data[0]) if self._data else 0
