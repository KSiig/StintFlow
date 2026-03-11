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

            # only operate on editors when their desired state differs from current
            stint_type_index = self.table_model.index(row, ColumnIndex.STINT_TYPE)
            # avoid str(None) producing "None" which is truthy when stripped
            val = stint_type_index.data()
            if val is None:
                has_text = False
            else:
                has_text = bool(str(val).strip())
            is_open = self.stint_table.table.isPersistentEditorOpen(stint_type_index)
            if lock_enabled and is_completed:
                if is_open:
                    self.stint_table.table.closePersistentEditor(stint_type_index)
            else:
                if has_text and not is_open:
                    self.stint_table.table.openPersistentEditor(stint_type_index)
                elif not has_text and is_open:
                    self.stint_table.table.closePersistentEditor(stint_type_index)

            tires_index = self.table_model.index(row, ColumnIndex.TIRES_CHANGED)
            is_open = self.stint_table.table.isPersistentEditorOpen(tires_index)
            if lock_enabled and is_completed:
                if is_open:
                    self.stint_table.table.closePersistentEditor(tires_index)
            else:
                if not is_open:
                    self.stint_table.table.openPersistentEditor(tires_index)

        self.stint_table._set_column_widths()

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
