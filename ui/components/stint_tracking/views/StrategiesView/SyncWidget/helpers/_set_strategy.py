"""Update the sync widget to reflect the active strategy."""

from __future__ import annotations


def _set_strategy(self, strategy: dict = None) -> None:
    """Show or hide the last sync label based on the active strategy data."""
    if self.last_sync_label is None:
        return

    last_sync = strategy.get("last_sync") if strategy else None
    label_text = self._format_last_sync_text(last_sync)

    if label_text is None:
        self.last_sync_label.clear()
        self.last_sync_label.hide()
        return

    self.last_sync_label.setText(label_text)
    self.last_sync_label.show()