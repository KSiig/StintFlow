from __future__ import annotations

from core.errors import log, log_exception
from ui.models.table_constants import ColumnIndex


def _open_persistent_editors(self) -> None:
    """Open persistent editors for editable columns respecting locks."""
    try:
        row_count = self.table_model.rowCount()
        lock_enabled = getattr(self, '_lock_completed', False)

        for row in range(row_count):
            status_idx = self.table_model.index(row, ColumnIndex.STATUS)
            status_val = status_idx.data()
            is_completed = status_val is not None and "Completed" in str(status_val)

            stint_type_index = self.table_model.index(row, ColumnIndex.STINT_TYPE)
            cell_text = str(stint_type_index.data())
            if lock_enabled and is_completed:
                self.stint_table.table.closePersistentEditor(stint_type_index)
            else:
                if cell_text:
                    self.stint_table.table.openPersistentEditor(stint_type_index)
                else:
                    self.stint_table.table.closePersistentEditor(stint_type_index)

            tires_index = self.table_model.index(row, ColumnIndex.TIRES_CHANGED)
            if lock_enabled and is_completed:
                self.stint_table.table.closePersistentEditor(tires_index)
            else:
                self.stint_table.table.openPersistentEditor(tires_index)

        self.stint_table.table.resizeColumnsToContents()

        log(
            'DEBUG',
            f'Opened persistent editors for {row_count} rows',
            category='strategy_tab',
            action='open_persistent_editors',
        )
    except Exception as e:
        log_exception(
            e,
            'Failed to open persistent editors',
            category='strategy_tab',
            action='open_persistent_editors',
        )
