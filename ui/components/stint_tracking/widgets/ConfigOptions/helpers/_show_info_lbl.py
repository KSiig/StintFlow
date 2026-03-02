from __future__ import annotations


def _show_info_lbl(self, text: str) -> None:
    """Show return-to-garage warning and flash taskbar."""
    self.lbl_info.show()
    self.lbl_info.setText(text)
    self._flash_taskbar()
