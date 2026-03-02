"""Create the tire combo editor with popup."""

from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QAbstractItemView, QHBoxLayout, QSizePolicy, QWidget

from ui.components.common.ConfigButton import ConfigButton
from ui.components.stint_tracking.delegates.TireComboDelegate.TirePopup import TirePopup
from ui.models.table_constants import ColumnIndex
from ui.models.TableRoles import TableRoles


def create_editor(self, parent, option, index):
    editor = QWidget(parent)
    editor.setAutoFillBackground(True)
    editor.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    editor.setPalette(option.palette)
    bg_color = option.palette.color(option.palette.ColorRole.Base).name()
    editor.setStyleSheet(f"QWidget#TireComboDelegate {{ background-color: {bg_color}; }}")
    editor.setObjectName("TireComboDelegate")

    layout = QHBoxLayout(editor)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    btn = ConfigButton(parent=editor, width_type="third")
    btn.setObjectName("TirePicker")
    btn.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    self._update_button_text(btn, index)
    layout.addWidget(btn)

    if self.lock_completed:
        status_idx = index.siblingAtColumn(ColumnIndex.STATUS)
        status = status_idx.data()
        if status is not None and "Completed" in str(status):
            btn.setEnabled(False)

    popup = TirePopup(editor)

    def show_popup():
        view = self._find_view(editor)
        if not view:
            return
        pos = btn.mapToGlobal(btn.rect().bottomLeft())
        pos.setY(pos.y() + 4)
        value = index.data(TableRoles.TiresRole)
        popup.set_values(value)
        popup.move(pos)
        popup.show()

    popup.dataChanged.connect(lambda: self.commitData.emit(editor))
    btn.clicked.connect(show_popup)

    editor.popup = popup
    editor.btn = btn

    if not self.strategy_id:
        QTimer.singleShot(0, show_popup)

    return editor
