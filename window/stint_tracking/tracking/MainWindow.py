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

class MainWindow(QWidget):
    def __init__(self, selection_model):
        super().__init__()

        self.selection_model = selection_model

        main_window = QVBoxLayout(self)

        session_picker = SessionPicker(selection_model=self.selection_model)
        stint_tracker = StintTracker(selection_model=self.selection_model)
        main_window.addWidget(session_picker)
        main_window.addWidget(stint_tracker)