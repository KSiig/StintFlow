from __future__ import annotations


def _reset_info_lbl(self) -> None:
    """Hide garage warning label."""
    self.lbl_info.setText("")
    self.lbl_info.hide()
