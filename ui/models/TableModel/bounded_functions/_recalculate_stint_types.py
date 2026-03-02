from ui.models.table_processors import recalculate_stint_types


def _recalculate_stint_types(self) -> None:
    """Recalculate stint types for all rows based on tire changes."""
    recalculate_stint_types(
        self._data,
        self.index,
        self.rowCount,
        self.editorsNeedRefresh.emit,
        self.dataChanged.emit,
        self._repaint_table,
    )
