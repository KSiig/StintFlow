"""Item flag handling for TableModel."""

from PyQt6.QtCore import Qt

from ui.models.table_constants import ColumnIndex
from ui.models.table_utils import is_completed_row


def flags(self, index):  # type: ignore[override]
    """Return item flags for a cell."""
    if not index.isValid():
        return Qt.ItemFlag.NoItemFlags

    editable_columns = {ColumnIndex.STINT_TYPE, ColumnIndex.TIRES_CHANGED}
    is_editable = self.editable and index.column() in editable_columns and (
        not self.partial or is_completed_row(self._data, index.row())
    )

    if is_editable:
        return self._get_editable_flags()

    return Qt.ItemFlag.NoItemFlags
