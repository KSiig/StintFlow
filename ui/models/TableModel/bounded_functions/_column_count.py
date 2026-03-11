"""Column count implementation for TableModel."""

from PyQt6.QtCore import QModelIndex


def columnCount(self, parent: QModelIndex = QModelIndex) -> int:  # type: ignore[override]
    """Return number of columns in model."""
    return len(self._data[0]) if self._data else 0
