"""Replace popup items and keep current value when possible."""

from PyQt6.QtGui import QIcon
from .set_value import set_value


def set_items(self, items: list[str]) -> None:
    """Replace popup items and keep current value when possible."""
    self._raw_items = items

    self.items = self._normalize_items(items)
    if self.sort_items:
        self.items.sort(key=lambda d: d['display'].lower())

    self.value_to_display = {d['value']: d['display'] for d in self.items}
    self.value_to_icon = {d['value']: d['icon'] for d in self.items}

    current_value = self.btn.text()
    self.popup.setParent(None)
    self.popup.deleteLater()
    self.popup = self._create_popup()
    self.popup.valueChanged.connect(self._on_value_changed)

    if current_value in self.value_to_display:
        disp = self.value_to_display.get(current_value)
        self.btn.setText(self._pad_text(disp))
        ico = self.value_to_icon.get(current_value)
        if ico:
            self.btn.setIcon(ico)
    elif self.items:
        first_val = self.items[0]['value']
        self.btn.setText(self._pad_text(self.items[0]['display']))
        ico = self.items[0].get('icon')
        if ico:
            self.btn.setIcon(ico)
        set_value(self, first_val)
    else:
        self.btn.setText("")
        self.btn.setIcon(QIcon())
