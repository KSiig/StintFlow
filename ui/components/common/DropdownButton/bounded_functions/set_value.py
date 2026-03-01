"""Set the current internal value and update display/icon."""

from PyQt6.QtGui import QIcon


def set_value(self, value: str) -> None:
    """Set the current internal value and update display/icon."""
    if value in self.value_to_display.values():
        for val, disp in self.value_to_display.items():
            if disp == value:
                value = val
                break
    self.current_value = value
    disp = self.value_to_display.get(value, value)
    self.btn.setText(self._pad_text(disp))
    ico = self.value_to_icon.get(value)
    if ico:
        self.btn.setIcon(ico)
    else:
        self.btn.setIcon(QIcon())
