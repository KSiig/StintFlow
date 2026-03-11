"""Handle editing and custom roles in TableModel.setData."""

from PyQt6.QtCore import Qt

from ui.models.TableRoles import TableRoles
from ui.models.table_constants import ColumnIndex


def setData(self, index, value, role: int = Qt.ItemDataRole.EditRole):  # type: ignore[override]
    """Update data for a specific cell."""
    if not index.isValid() or role not in (Qt.ItemDataRole.EditRole, TableRoles.TiresRole, TableRoles.MetaRole):
        return False

    row = index.row()
    col = index.column()

    if role == Qt.ItemDataRole.EditRole:
        self._data[row][col] = value

    elif role == TableRoles.TiresRole:
        while row >= len(self._tires):
            self._tires.append({})
        self._tires[row] = value
        tires_changed = sum(value.get("tires_changed", {}).values())
        self._data[row][ColumnIndex.TIRES_CHANGED] = str(tires_changed)

    elif role == TableRoles.MetaRole:
        while row >= len(self._meta):
            self._meta.append({})
        self._meta[row] = value

    self.dataChanged.emit(index, index, [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole])
    return True
