"""
Dropdown button with value/data pairs for combo-like behavior.

Wraps DropdownButton and exposes a subset of QComboBox-like methods.
"""

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from ui.components.common import DropdownButton
from .bounded_functions import (
    addItem,
    blockSignals,
    clear,
    count,
    currentData,
    currentText,
    setCurrentIndex,
    findData,
    setFont,
    set_text_alignment_left,
    setFixedHeight,
)
from .helpers import (
    _refresh_items,
    _on_value_changed,
)


class DataDropdownButton(QWidget):
    """
    Dropdown button that stores (label, userData) items.

    Provides QComboBox-like methods used by SessionPicker.
    """

    currentIndexChanged = pyqtSignal(int)

    addItem = addItem
    clear = clear
    count = count
    currentData = currentData
    currentText = currentText
    setCurrentIndex = setCurrentIndex
    findData = findData
    blockSignals = blockSignals
    setFont = setFont
    set_text_alignment_left = set_text_alignment_left
    setFixedHeight = setFixedHeight

    _refresh_items = _refresh_items
    _on_value_changed = _on_value_changed

    def __init__(
        self,
        button_object_name: str = "DropdownButton",
        popup_object_name: str = "DropdownPopup",
        item_object_name: str = "DropdownPopupItem",
        parent: QWidget = None,
        load_styles: bool = True,
        sort_items: bool = True,
    ):
        super().__init__(parent)
        self._items: list[tuple[str, str | None]] = []
        self._current_index = -1
        self._signals_blocked = False
        self._sort_items = sort_items

        self.dropdown = DropdownButton(
            items=[],
            current_value="",
            button_object_name=button_object_name,
            popup_object_name=popup_object_name,
            item_object_name=item_object_name,
            load_styles=load_styles,
            sort_items=sort_items,
            parent=self,
        )
        self.dropdown.valueChanged.connect(self._on_value_changed)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.dropdown)
