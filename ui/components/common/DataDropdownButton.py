"""
Dropdown button with value/data pairs for combo-like behavior.

Wraps DropdownButton and exposes a subset of QComboBox-like methods.
"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtCore import pyqtSignal

from .DropdownButton import DropdownButton


class DataDropdownButton(QWidget):
    """
    Dropdown button that stores (label, userData) items.

    Provides QComboBox-like methods used by SessionPicker.
    """

    currentIndexChanged = pyqtSignal(int)

    def __init__(
        self,
        button_object_name: str = "DropdownButton",
        popup_object_name: str = "DropdownPopup",
        item_object_name: str = "DropdownPopupItem",
        parent=None,
        load_styles: bool = True
    ):
        super().__init__(parent)
        self._items: list[tuple[str, str]] = []
        self._current_index = -1
        self._signals_blocked = False

        self.dropdown = DropdownButton(
            items=[],
            current_value="",
            button_object_name=button_object_name,
            popup_object_name=popup_object_name,
            item_object_name=item_object_name,
            load_styles=load_styles,
            parent=self
        )
        self.dropdown.valueChanged.connect(self._on_value_changed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.dropdown)

    def addItem(self, text: str, userData: str = None) -> None:
        """Add a new item with optional user data."""
        self._items.append((text, userData))
        self._refresh_items(emit=False)

        if self._current_index == -1 and self._items:
            self.setCurrentIndex(0)

    def clear(self) -> None:
        """Clear all items and reset selection."""
        self._items = []
        self._current_index = -1
        self.dropdown.set_items([])
        self.dropdown.set_value("")

    def count(self) -> int:
        """Return the number of items."""
        return len(self._items)

    def currentData(self):
        """Return user data for the current item."""
        if self._current_index < 0:
            return None
        return self._items[self._current_index][1]

    def currentText(self) -> str:
        """Return label text for the current item."""
        if self._current_index < 0:
            return ""
        return self._items[self._current_index][0]

    def setCurrentIndex(self, index: int) -> None:
        """Set current selection by index."""
        if index < 0 or index >= len(self._items):
            self._current_index = -1
            self.dropdown.set_value("")
        else:
            self._current_index = index
            self.dropdown.set_value(self._items[index][0])

        if not self._signals_blocked:
            self.currentIndexChanged.emit(self._current_index)

    def findData(self, value) -> int:
        """Find index by user data value."""
        for index, (_, data) in enumerate(self._items):
            if data == value or str(data) == str(value):
                return index
        return -1

    def blockSignals(self, blocked: bool) -> bool:
        """Block/unblock signals for this widget."""
        self._signals_blocked = blocked
        return super().blockSignals(blocked)

    def setFont(self, font) -> None:
        """Set font on the underlying button."""
        self.dropdown.btn.setFont(font)

    def set_text_alignment_left(self, padding_left: int = 0) -> None:
        """Left-align the text inside the button with optional padding."""
        self.dropdown.set_text_alignment_left(padding_left=padding_left)

    def setFixedHeight(self, height: int) -> None:
        """Set a fixed height for the button."""
        super().setFixedHeight(height)
        self.dropdown.btn.setFixedHeight(height)

    def _refresh_items(self, emit: bool = True) -> None:
        labels = [label for label, _ in self._items]
        self.dropdown.set_items(labels)

        if self._current_index >= len(self._items):
            self._current_index = -1
            self.dropdown.set_value("")

        if emit and not self._signals_blocked:
            self.currentIndexChanged.emit(self._current_index)

    def _on_value_changed(self, value: str) -> None:
        index = -1
        for i, (label, _) in enumerate(self._items):
            if label == value:
                index = i
                break

        self._current_index = index

        if not self._signals_blocked:
            self.currentIndexChanged.emit(self._current_index)
