from __future__ import annotations


def _hide_placeholder(self) -> None:
    """Hide placeholder and ensure widths are applied."""
    self._placeholder_label.hide()
    self.table.show()
    self._set_column_widths()
