from __future__ import annotations


def _refresh_editors(self) -> None:
    """Refresh persistent editors for stint type column."""
    if self.table.model() is None:
        return

    self._hide_placeholder()

    for row in range(self.table.model().rowCount()):
        index = self.table.model().index(row, 0)
        cell_text = str(index.data())
        if cell_text:
            self.table.openPersistentEditor(index)
        else:
            self.table.closePersistentEditor(index)
