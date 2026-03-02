"""Create the stint type editor widget."""

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QAbstractItemView, QHBoxLayout, QSizePolicy, QWidget

from ui.components.common import DropdownButton
from ui.models.table_constants import ColumnIndex
from ui.utilities import FONT, get_fonts


def create_editor(self, parent, option, index):
    editor = QWidget(parent)
    editor.setAutoFillBackground(True)
    editor.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    editor.setPalette(option.palette)
    bg_color = option.palette.color(option.palette.ColorRole.Base).name()
    editor.setStyleSheet(f"QWidget#StintTypeComboEditor {{ background-color: {bg_color}; }}")
    editor.setObjectName("StintTypeComboEditor")

    layout = QHBoxLayout(editor)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    dropdown = DropdownButton(items=self.items, current_value=str(index.data()) or "", sort_items=False, parent=editor)
    dropdown.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    dropdown.btn.setFont(get_fonts(FONT.table_cell))
    dropdown.btn.setStyleSheet("text-align: left; padding-left: 8px;")

    current_text = str(index.data())
    if current_text == "":
        dropdown.btn.setEnabled(False)
    if self.lock_completed:
        status_idx = index.siblingAtColumn(ColumnIndex.STATUS)
        status = status_idx.data()
        if status is not None and "Completed" in str(status):
            dropdown.btn.setEnabled(False)

    dropdown.valueChanged.connect(lambda: self.commitData.emit(editor))
    layout.addWidget(dropdown)

    editor.dropdown = dropdown

    if not self.strategy_id:
        QTimer.singleShot(0, lambda: dropdown.btn.click())
        dropdown.valueChanged.connect(lambda: self.closeEditor.emit(editor))

    return editor
