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
from ..delegates import TireComboDelegate, StintTypeCombo
from helpers.strategies import get_strategies, mongo_docs_to_rows
from helpers import clear_layout

class MainWindow(QWidget):
    def __init__(self, models = {"selection_model": SelectionModel()}):
        super().__init__()

        self.selection_model = models['selection_model']
        self.table_model = models['table_model']
        self.models = models
        self.selection_model.sessionChanged.connect(self.create_view)

        self.main_layout = QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.create_view()

    def create_view(self):
        clear_layout(self.main_layout)
        session_id = self.selection_model.session_id
        strategies = list(get_strategies(session_id))

        main_tab = MainTab(self.models)
        main_tab.strategy_created.connect(self.insert_tab)

        self.tabs = QTabWidget(self)
        self.tabs.addTab(main_tab, "Main")

        if strategies:
            for strategy in strategies:
                tab = self.create_tab(strategy, self.models)

                self.tabs.addTab(tab, strategy['name'])

        self.main_layout.addWidget(self.tabs)


    def create_tab(self, strategy, models):
        first_stint = strategy['model_data']['rows']
        strategy_data = mongo_docs_to_rows(first_stint)
        table_model = self.table_model.clone()
        tracker_models = {
            **self.models,
            "table_model": table_model
        }

        stint_tracker = StintTracker(tracker_models, auto_update=False)
        stint_tracker.table.setItemDelegateForColumn(
            0,
            StintTypeCombo(stint_tracker.table, update_doc=True, strategy_id=strategy['_id'])
        )
        stint_tracker.table.setItemDelegateForColumn(
            4,
            TireComboDelegate(stint_tracker.table, update_doc=True, strategy_id=strategy['_id'])
        )
        tab = QWidget()

        layout = QVBoxLayout()
        tab.setLayout(layout)
        tracker_models['table_model'].update_data(strategy_data, strategy['model_data']['tires'])
        layout.addWidget(stint_tracker)
        for row in range(stint_tracker.table.model().rowCount()):
            index = stint_tracker.table.model().index(row, 0)  # 0 = stint_type column
            cell_text = str(index.data())

            if cell_text:  # non-empty → open editor
                stint_tracker.table.openPersistentEditor(index)
            else:  # empty → close editor
                stint_tracker.table.closePersistentEditor(index)
            # index = stint_tracker.table.model().index(row, 0)
            # stint_tracker.table.openPersistentEditor(index)
            index = stint_tracker.table.model().index(row, 4)
            stint_tracker.table.openPersistentEditor(index)
        stint_tracker.table.resizeColumnsToContents()

        return tab

    def insert_tab(self, strategy):
        tab = self.create_tab(strategy, self.models)

        self.tabs.addTab(tab, strategy['name'])