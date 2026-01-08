from PyQt6.QtWidgets import ( 
        QMainWindow, 
        QTableView, 
        QGridLayout,
        QPushButton, 
        QWidget, 
        QVBoxLayout, 
        QHBoxLayout, 
        QPlainTextEdit, 
        QTabWidget,
        QComboBox, 
        QLineEdit, 
        QLabel
    )
from ..SessionPicker import SessionPicker
from ..StintTracker import StintTracker
from ...models import NavigationModel, SelectionModel
from .MainTab import MainTab
from ..delegates.TireChangeCombo import TireComboDelegate
from helpers.strategies import get_strategies, mongo_docs_to_rows

class MainWindow(QWidget):
    def __init__(self, models = {"selection_model": SelectionModel()}):
        super().__init__()

        self.selection_model = models['selection_model']
        self.table_model = models['table_model']
        self.models = models

        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)

        session_picker = SessionPicker(models)
        main_layout.addWidget(session_picker)

        session_id = self.selection_model.session_id
        strategies = list(get_strategies(session_id))

        main_tab = MainTab(self.models)
        main_tab.strategy_created.connect(self.insert_tab)

        self.tabs = QTabWidget(self)
        self.tabs.addTab(main_tab, "Main")

        if strategies:
            for strategy in strategies:
                tab = self.create_tab(strategy, models)

                self.tabs.addTab(tab, strategy['name'])

        main_layout.addWidget(self.tabs)

    def create_tab(self, strategy, models):
        first_stint = strategy['model_data']
        strategy_data = mongo_docs_to_rows(first_stint)
        table_model = self.table_model.clone()
        self.models['table_model'] = table_model

        stint_tracker = StintTracker(models)
        stint_tracker.table.setItemDelegateForColumn(
            3,
            TireComboDelegate(stint_tracker.table, update_doc=True, strategy_id=strategy['_id'])
        )
        tab = QWidget()

        layout = QVBoxLayout()
        tab.setLayout(layout)
        self.models['table_model'].update_data(strategy_data)
        layout.addWidget(stint_tracker)
        for row in range(stint_tracker.table.model().rowCount()):
            index = stint_tracker.table.model().index(row, 3)
            stint_tracker.table.openPersistentEditor(index)
        stint_tracker.table.resizeColumnsToContents()

        return tab

    def insert_tab(self, strategy):
        tab = self.create_tab(strategy, self.models)

        self.tabs.addTab(tab, strategy['name'])