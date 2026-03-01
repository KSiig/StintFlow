"""
Reusable dropdown button widget with custom popup.
"""

from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import pyqtSignal

from .bounded_functions import (
    get_value,
    set_items,
    set_sorting,
    set_text_alignment_left,
    set_value,
)
from .helpers import (
    DropdownPopup,
    _normalize_items,
    _on_value_changed,
    _pad_text,
    _setup_styles,
    _show_popup,
)


class DropdownButton(QWidget):
    """Custom dropdown button with popup selection menu."""

    valueChanged = pyqtSignal(str)

    set_sorting = set_sorting
    set_value = set_value
    set_text_alignment_left = set_text_alignment_left
    set_items = set_items
    get_value = get_value

    _setup_styles = _setup_styles
    _normalize_items = _normalize_items
    _pad_text = _pad_text
    _show_popup = _show_popup
    _on_value_changed = _on_value_changed

    def __init__(
        self,
        items: list[str],
        current_value: str = "",
        button_object_name: str = "DropdownButton",
        popup_object_name: str = "DropdownPopup",
        item_object_name: str = "DropdownPopupItem",
        load_styles: bool = True,
        sort_items: bool = True,
        parent=None,
    ):
        super().__init__(parent)

        if load_styles:
            self._setup_styles()

        self._raw_items = items
        self.sort_items = sort_items

        self.items = self._normalize_items(items)
        if self.sort_items:
            self.items.sort(key=lambda d: d['display'].lower())

        self.value_to_display = {d['value']: d['display'] for d in self.items}
        self.value_to_icon = {d['value']: d['icon'] for d in self.items}

        self.button_object_name = button_object_name
        self.popup_object_name = popup_object_name
        self.item_object_name = item_object_name

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.btn = QPushButton("")
        self.btn.setObjectName(button_object_name)
        self.btn.clicked.connect(self._show_popup)
        layout.addWidget(self.btn)

        self.current_value = None

        if current_value is not None:
            self.set_value(current_value)

        self.popup = self._create_popup()
        self.popup.valueChanged.connect(self._on_value_changed)

    def _create_popup(self) -> DropdownPopup:
        """Create a dropdown popup instance."""
        return DropdownPopup(
            items=self.items,
            popup_object_name=self.popup_object_name,
            item_object_name=self.item_object_name,
            parent=self,
        )
