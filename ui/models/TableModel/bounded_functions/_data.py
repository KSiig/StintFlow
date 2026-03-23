"""Cell data retrieval for TableModel."""

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor

from ui.utilities import FONT, get_fonts
from ui.models.TableRoles import TableRoles


def data(self, index, role: int = Qt.ItemDataRole.DisplayRole):  # type: ignore[override]
    """Retrieve data for a specific cell and role."""
    if not index.isValid():
        return None

    row = index.row()
    col = index.column()

    if row >= len(self._data) or (self._data and col >= len(self._data[row])):
        return None

    if role == Qt.ItemDataRole.DisplayRole:
        return self._data[row][col]

    if role == Qt.ItemDataRole.BackgroundRole:
        meta = self._meta[row] if row < len(self._meta) else None
        if isinstance(meta, dict) and meta.get("excluded"):
            return QColor("#281F23")

    if role == Qt.ItemDataRole.FontRole:
        return get_fonts(FONT.text_ui)

    if role == Qt.ItemDataRole.TextAlignmentRole:
        return Qt.AlignmentFlag.AlignVCenter

    if role == TableRoles.TiresRole:
        return self._tires[row] if row < len(self._tires) else None

    if role == TableRoles.MetaRole:
        return self._meta[row] if row < len(self._meta) else None

    return None
