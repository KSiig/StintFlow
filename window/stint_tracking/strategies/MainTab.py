from PyQt6.QtWidgets import ( 
        QMainWindow, 
        QTableView, 
        QGridLayout,
        QPushButton, 
        QWidget, 
        QVBoxLayout, 
        QHBoxLayout, 
        QPlainTextEdit, 
        QComboBox, 
        QLineEdit, 
        QLabel,
        QHeaderView,
        QAbstractButton,
        QTabWidget,
        QAbstractItemView,
        QSizePolicy
    )

from PyQt6.QtCore import QProcess, QTimer, Qt, QSize
from PyQt6.QtGui import QIcon
from helpers.stinttracker import get_stints, get_event
from helpers import stints_to_table, resource_path
from window.models import TableModel
from ...TitleBar import TitleBar
from ...Fonts import FONT, get_fonts
from ...models import NavigationModel, SelectionModel
from ..StintTracker import StintTracker

class MainTab(QWidget):
    def __init__(self, models = {"selection_model": SelectionModel()}):
        super().__init__()

        self.selection_model = models['selection_model']

        main_layout = QGridLayout(self)
        self.setLayout(main_layout)

        tab = QTabWidget(self)

        stint_tracker = StintTracker(models)
        page = QWidget(tab)

        layout = QVBoxLayout()
        page.setLayout(layout)
        label = QLabel("Hello world")
        layout.addWidget(stint_tracker)

        page1 = QWidget(tab)

        layout1 = QVBoxLayout()
        page1.setLayout(layout1)
        label1 = QLabel("Hello world")
        layout1.addWidget(label1)

        tab.addTab(page, 'Test tab')
        tab.addTab(page1, 'New tab')

        main_layout.addWidget(tab)
