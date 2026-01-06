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
from helpers.strategies import get_strategies
from datetime import timedelta

class MainWindow(QWidget):
    def __init__(self, models = {"selection_model": SelectionModel()}):
        super().__init__()

        self.selection_model = models['selection_model']
        self.table_model = models['table_model']
        self.models = models

        session_id = self.selection_model.session_id
        strategies = list(get_strategies(session_id))
        main_layout = QVBoxLayout(self)
        self.setLayout(main_layout)
        session_picker = SessionPicker(models)
        main_layout.addWidget(session_picker)
        if strategies:
            strategy = strategies[0]
            first_stint = strategy['model_data']
            strategy_data = self.mongo_docs_to_rows(first_stint)
            table_model = self.table_model.clone()
            self.models['table_model'] = table_model


            tabs = QTabWidget(self)

            stint_tracker = StintTracker(models)
            stint_tracker.table.setItemDelegateForColumn(
                3,
                TireComboDelegate(stint_tracker.table, update_doc=True, strategy_id=strategy['_id'])
            )
            page = QWidget(tabs)

            layout = QVBoxLayout()
            page.setLayout(layout)
            self.models['table_model'].update_data(strategy_data)
            layout.addWidget(stint_tracker)
            for row in range(stint_tracker.table.model().rowCount()):
                index = stint_tracker.table.model().index(row, 3)
                stint_tracker.table.openPersistentEditor(index)
            stint_tracker.table.resizeColumnsToContents()

            tabs.addTab(page, 'Test tab')
            main_layout.addWidget(tabs)


    def mongo_docs_to_rows(self, docs):
        rows = []

        for doc in docs:
            row = [
                doc.get("name"),
                "✅" if doc.get("driven") else "❌",
                doc.get("pit_end_time"),
                int(doc.get("tires_changed", 0)),
                int(doc.get("tires_left", 0)),
                timedelta(seconds=int(doc.get("stint_time_seconds", 0))),
            ]
            rows.append(row)

        return rows
