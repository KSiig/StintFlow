def _repaint_table(self) -> None:
    """Emit dataChanged signal for entire table when dimensions unchanged."""
    if self.rowCount() > 0 and self.columnCount() > 0:
        top_left = self.index(0, 0)
        bottom_right = self.index(self.rowCount() - 1, self.columnCount() - 1)
        self.dataChanged.emit(top_left, bottom_right, [])
