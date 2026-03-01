"""Handle value change emitted by the popup."""

from PyQt6.QtGui import QIcon


def _on_value_changed(self, value: str) -> None:
    """Store internal value and update button display/icon."""
    self.current_value = value
    disp = self.value_to_display.get(value, value)
    self.btn.setText(self._pad_text(disp))
    ico = self.value_to_icon.get(value)
    if ico:
        self.btn.setIcon(ico)
    else:
        self.btn.setIcon(QIcon())
    self.valueChanged.emit(value)
