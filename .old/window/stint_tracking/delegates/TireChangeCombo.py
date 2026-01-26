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
from helpers.stinttracker.races import update_stint
from helpers.strategies import sanitize_stints, update_strategy
from ...models import TableRoles
import json
import copy

class TireComboDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, update_doc=False, strategy_id=None):
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
        self.update_btn(editor.btn, index)
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        values = editor.popup.values()
        values_lowered = {k.lower(): v.lower() for k, v in values.items()}
        old_value = model.data(index, TableRoles.TiresRole)
        new_value = copy.deepcopy(old_value)

        for tire, compound in values_lowered.items():
            new_value['tires_changed'][tire] = bool(compound)
            if compound:
                new_value[tire.lower()]['outgoing']['compound'] = compound

        if new_value == old_value:
            return  # ← prevents duplicate trigger

        model.setData(index, new_value, TableRoles.TiresRole)
        model.recalc_tires_left()
        row_data, tire_data = model.get_all_data()
        sanitized_data = sanitize_stints(row_data, tire_data)
        if self.strategy_id:
            update_strategy(self.strategy_id, sanitized_data)
        else:
            stint_id = model.data(index, TableRoles.MetaRole)['id']
            row = sanitized_data['tires'][index.row()]
            update_stint(stint_id, row)

    def update_btn(self, btn, index):
        tire_data = index.data(TableRoles.TiresRole)
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
        btn_medium.clicked.connect(lambda: self.set_all_tires("medium"))
        btn_wet.clicked.connect(lambda: self.set_all_tires("wet"))

        for btn in (btn_medium, btn_wet, btn_x):
            btn.setFixedSize(SIZE_BTN)
            btn.setIconSize(SIZE_ICON)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(0)

        btn_layout.addWidget(btn_x)
        btn_layout.addWidget(btn_medium)
        btn_layout.addWidget(btn_wet)

        layout.addLayout(btn_layout, 0, 1)

        self.boxes = {}
        for i, tire in enumerate(["FL", "FR", "RL", "RR"]):
            row = (i // 2) + 1      # 0, 0, 1, 1
            col = (i % 2) * 2 # 0, 2 (label + checkbox)

            label = QLabel(tire)
            cb = QComboBox()
            cb.addItems(["", "Medium", "Wet", "Used medium", "Used wet"])
            cb.currentIndexChanged.connect(lambda _: self.dataChanged.emit())

            layout.addWidget(label, row, col)
            layout.addWidget(cb, row, col + 1)

            self.boxes[tire] = cb

    def setValues(self, data):
        for tire, _ in self.boxes.items():
            if tire in self.boxes:
                tire_changed = data['tires_changed'][tire.lower()]
                tire_compound = data[tire.lower()]['outgoing']['compound'].capitalize()
                index = self.boxes[tire].findText(tire_compound)
                if tire_changed:
                    index = self.boxes[tire].findText(tire_compound)
                    self.boxes[tire].setCurrentIndex(index)
                else:
                    self.boxes[tire].setCurrentIndex(0)


    def values(self):
        return {k: v.currentText() for k, v in self.boxes.items()}

    def set_all_tires(self, compound):
        for tire, _ in self.boxes.items():
            if tire in self.boxes:
                if compound:
                    index = self.boxes[tire].findText(compound.capitalize())
                    self.boxes[tire].setCurrentIndex(index)
                else:
                    self.boxes[tire].setCurrentIndex(0)
                self.dataChanged.emit()
