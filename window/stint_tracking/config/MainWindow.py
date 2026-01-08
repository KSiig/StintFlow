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
from .ConfigOptions import ConfigOptions

class MainWindow(QWidget):
    def __init__(self, models = {"selection_model": SelectionModel()}):
        super().__init__()

        self.selection_model = models['selection_model']

        main_window = QVBoxLayout(self)

        h_layout = QHBoxLayout()
        config_options = ConfigOptions(models)
        stint_tracker = StintTracker(models)

        h_layout.addWidget(config_options)
        h_layout.addWidget(stint_tracker)

        main_window.addLayout(h_layout)