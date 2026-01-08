from PyQt6.QtWidgets import ( 
        QMainWindow, 
        QTableView, 
        QPushButton, 
        QWidget, 
        QVBoxLayout, 
        QHBoxLayout, 
        QPlainTextEdit, 
        QComboBox, 
        QLineEdit, 
        QLabel
    )

from ..SessionPicker import SessionPicker
from ..StintTracker import StintTracker
from ...models import NavigationModel, SelectionModel

class MainWindow(QWidget):
    def __init__(self, models = {"selection_model": SelectionModel()}):
        super().__init__()

        self.selection_model = models['selection_model']

        main_window = QVBoxLayout(self)

        stint_tracker = StintTracker(models)
        main_window.addWidget(stint_tracker)