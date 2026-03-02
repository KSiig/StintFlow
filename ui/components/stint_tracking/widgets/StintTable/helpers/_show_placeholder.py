from __future__ import annotations


def _show_placeholder(self) -> None:
    """Show placeholder when no rows exist."""
    self.table.hide()
    self._placeholder_label.show()
