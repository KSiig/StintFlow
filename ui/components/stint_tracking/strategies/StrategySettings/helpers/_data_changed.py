from __future__ import annotations


def _data_changed(self, *_args) -> None:
    """Sync input widgets when table data changes."""
    self._set_inputs()
