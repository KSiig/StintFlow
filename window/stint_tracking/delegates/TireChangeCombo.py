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
from helpers.strategies import sanitize_stints, update_strategy

class TireComboDelegate(QStyledItemDelegate):
    def __init__(self, parent=None, update_doc=False, strategy_id=""):
        super().__init__(parent)
        self.update_doc = update_doc
        self.strategy_id = strategy_id

    def createEditor(self, parent, option, index):
        combo = QComboBox(parent)
        combo.addItems(["0", "1", "2", "3", "4"])

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
        model.setData(index, editor.currentText())
        model.recalc_tires()
        sanitized_data = sanitize_stints(model.get_all_data())
        update_strategy(self.strategy_id, sanitized_data)