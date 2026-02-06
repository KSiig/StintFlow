from PyQt6.QtWidgets import ( 
        QMainWindow, 
        QTableView, 
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
from PyQt6.QtCore import Qt
from helpers.strategies import sanitize_stints, update_strategy

class StintTypeCombo(QStyledItemDelegate):
    def __init__(self, parent=None, update_doc=False, strategy_id=None):
        super().__init__(parent)
        self.update_doc = update_doc
        self.strategy_id = strategy_id
        self.items = ["", "Single", "Double", "Triple", "Quadruple", "Quintuple", 
                      "Sextuple", "Septuple", "Octuple", "Nonuple", "Decuple"]

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.setObjectName("StintTypeCombo")
        combo.addItems(self.items)

        # Disable if the current cell text is empty
        current_text = str(index.data())
        if current_text == "":
            combo.setEnabled(False)
            combo.setStyleSheet("color: gray;")

        # Commit on every change
        combo.currentTextChanged.connect(
            lambda _: self.commitData.emit(combo)
        )

        return combo

    def setEditorData(self, editor, index):
        editor.blockSignals(True)
        editor.setCurrentText(str(index.data()))
        editor.blockSignals(False)

    def setModelData(self, editor, model, index):
        old_value = model.data(index, Qt.ItemDataRole.DisplayRole)
        new_value = editor.currentText()

        if new_value == old_value:
            return  # ← prevents duplicate trigger

        model.setData(index, new_value)
        model.recalc_tires_changed(index, old_value)
        if self.strategy_id:
            row_data, tire_data = model.get_all_data()
            sanitized_data = sanitize_stints(row_data, tire_data)
            update_strategy(self.strategy_id, sanitized_data)
        else:
            print("not a strategy")