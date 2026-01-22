from PyQt6.QtWidgets import ( 
        QMainWindow, 
        QSizePolicy,
        QCheckBox,
        QTableView, 
        QAbstractItemView,
        QFrame,
        QGridLayout,
        QPushButton, 
        QWidget, 
        QVBoxLayout, 
        QHBoxLayout, 
        QPlainTextEdit, 
        QStyledItemDelegate,
        QTabWidget,
        QComboBox, 
        QLineEdit, 
        QLabel
    )
from PyQt6.QtCore import Qt, pyqtSignal, QSize
from PyQt6.QtGui import QPixmap, QIcon
from helpers import resource_path
from helpers.strategies import sanitize_stints, update_strategy
from ...models import TableRoles
import json
import copy

class TireComboDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, update_doc=False, strategy_id=""):
        super().__init__(parent)
        self.update_doc = update_doc
        self.strategy_id = strategy_id
        self.tires_changed = "0"

    def createEditor(self, parent, option, index):
        editor = QWidget(parent)
        layout = QHBoxLayout(editor)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        btn = QPushButton(editor)
        btn.setObjectName("TirePicker")
        btn.setSizePolicy(
            QSizePolicy.Policy.Expanding,  # width adjusts to minimum needed
            QSizePolicy.Policy.Expanding   # height adjusts to fit content
        )
        self.update_btn(btn, index)
        layout.addWidget(btn)

        popup = TirePopup(editor)

        def show_popup():
            view = find_view(editor)
            if not view:
                return

            rect = view.visualRect(index)
            pos = view.viewport().mapToGlobal(rect.bottomLeft())

            value = index.data(TableRoles.TiresRole)
            popup.setValues(value)

            popup.move(pos)
            popup.show()

        def find_view(widget):
            while widget:
                if isinstance(widget, QAbstractItemView):
                    return widget
                widget = widget.parent()
            return None

        popup.dataChanged.connect(lambda: self.commitData.emit(editor))

        btn.clicked.connect(show_popup)

        editor.popup = popup
        editor.btn = btn
        return editor

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        self.tires_changed = index.data()
        # editor.setCurrentText(str(index.data()))
        self.update_btn(editor.btn, index)
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        values = editor.popup.values()
        values_lowered = {k.lower(): v for k, v in values.items()}
        old_value = model.data(index, TableRoles.TiresRole)
        new_value = copy.deepcopy(old_value)
        new_value['tires_changed'] = values_lowered

        if new_value == old_value:
            return  # ← prevents duplicate trigger

        model.setData(index, new_value, TableRoles.TiresRole)
        model.recalc_tires_left()
        row_data, tire_data = model.get_all_data()
        sanitized_data = sanitize_stints(row_data, tire_data)
        update_strategy(self.strategy_id, sanitized_data)

    def update_btn(self, btn, index):
        tire_data = index.data(TableRoles.TiresRole)
        # print("tire_data: ", tire_data)
        if tire_data:
            tires_changed = sum(tire_data['tires_changed'].values())
        else:
            tires_changed = 0

        btn.setText(str(tires_changed) + " New")


class TirePopup(QWidget):
    dataChanged = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Popup)
        layout = QGridLayout(self)

        SIZE_BTN = QSize(24, 24)
        SIZE_ICON = QSize(16, 16)

        btn_x = QPushButton("X")
        btn_x.setStyleSheet("font-weight: bold;")
        btn_medium = QPushButton()
        btn_medium.setIcon(QIcon(resource_path('resources/tire_icons/medium.png')))
        btn_wet = QPushButton()
        btn_wet.setIcon(QIcon(resource_path('resources/tire_icons/wet.png')))

        btn_x.clicked.connect(lambda: self.set_all_tires(None))
        btn_medium.clicked.connect(lambda: self.set_all_tires("mediums"))
        btn_wet.clicked.connect(lambda: self.set_all_tires("wets"))

        for btn in (btn_medium, btn_wet, btn_x):
            btn.setFixedSize(SIZE_BTN)
            btn.setIconSize(SIZE_ICON)

        layout.addWidget(btn_x, 0, 0)
        layout.addWidget(btn_medium, 0, 1)
        # layout.addWidget(btn_wet, 0, 2)

        self.boxes = {}
        for i, tire in enumerate(["FL", "FR", "RL", "RR"]):
            row = (i // 2) + 1      # 0, 0, 1, 1
            col = (i % 2) * 2 # 0, 2 (label + checkbox)

            label = QLabel(tire)
            cb = QCheckBox()
            cb.clicked.connect(lambda _: self.dataChanged.emit())

            layout.addWidget(label, row, col)
            layout.addWidget(cb, row, col + 1)

            self.boxes[tire] = cb

    def setValues(self, data):
        for tire, _ in self.boxes.items():
            if tire in self.boxes:
                tire_changed = data['tires_changed'][tire.lower()]
                self.boxes[tire].setChecked(tire_changed)

    def values(self):
        return {k: v.isChecked() for k, v in self.boxes.items()}

    def set_all_tires(self, tires):
        for tire, _ in self.boxes.items():
            if tire in self.boxes:
                tire_changed = bool(tires)
                self.boxes[tire].setChecked(tire_changed)
                self.dataChanged.emit()
