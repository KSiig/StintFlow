"""Row count implementation for TableModel."""

from PyQt6.QtCore import QModelIndex


def rowCount(self, parent: QModelIndex = None) -> int:  # type: ignore[override]
    """Return number of rows in model."""
    if parent is None:
        parent = QModelIndex()
    return len(self._data)
