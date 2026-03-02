from __future__ import annotations


def _set_active(self, active: bool) -> None:
    """Enable or disable add/remove/fetch buttons."""
    self.btn_add.setEnabled(active)
    self.btn_remove.setEnabled(active)
    self.btn_fetch.setEnabled(active)
