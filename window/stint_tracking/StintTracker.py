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
        QLabel,
        QHeaderView,
        QAbstractButton,
        QAbstractItemView,
        QSizePolicy
    )
from PyQt6.QtCore import QProcess, QTimer, Qt, QSize
from PyQt6.QtGui import QIcon
from helpers.stinttracker import get_stints, get_event
from helpers import stints_to_table, resource_path
from window.models import TableModel
from ..TitleBar import TitleBar
from ..Fonts import FONT, get_fonts
from ..models import NavigationModel, SelectionModel

class StintTracker(QWidget):

    def __init__(self, models = {"selection_model": SelectionModel()}, focus = False, auto_update=True):
        super().__init__()

        self.selection_model = models['selection_model']
        self.table_model = models['table_model']

        with open(resource_path('styles/stint_tracker.qss'), 'r') as f:
            style = f.read()

        self.setStyleSheet(style)

        container = QHBoxLayout(self)

        font_text_table_cell = get_fonts(FONT.text_table_cell)
        font_table_header = get_fonts(FONT.header_table)

        self.table = QTableView(self)
        self.table.setShowGrid(False)
        self.table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.table.headers = [
            "Stint type",
            "Driver",
            "Driven",
            "Pit end time",
            "Tires changed",
            "Tires left",
            "Stint time"
        ]
        self.table.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding
        )
        # self.table.setMinimumWidth(self.table.horizontalHeader().length())
        if not focus:
            self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
            self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.table_model.update_data()
        self.refresh_table()      # initial load
        self.table_model.editorsNeedRefresh.connect(self.refresh_editors)

        vh = self.table.verticalHeader()
        self.table.verticalHeader().setStyleSheet(
            f"QHeaderView::section {{ font-family: {font_text_table_cell.family()}; font-size: {font_text_table_cell.pointSize()}pt; }}"
        )
        vh.setFixedWidth(80)
        vh.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        # vh.setFont(font_small_text)

        hh = self.table.horizontalHeader()
        hh.setFont(font_table_header)


        corner = self.table.findChild(QAbstractButton)
        if corner:
            # Remove existing layout/content
            corner.setText("")
            corner.setIcon(QIcon())

            layout = QVBoxLayout()
            layout.setContentsMargins(2, 2, 2, 2)
            layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

            label = QLabel("Stint no.")
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            label.setFont(font_table_header)

            corner.setLayout(layout)
            layout.addWidget(label)

            corner.setFixedWidth(80)
        
        self.table.setObjectName("StintsTable")

        ### REGION - LAYOUTS ###
        
        container.addWidget(self.table)

        # self.timer = QTimer(self)
        # self.timer.setInterval(5000)  # 1 second
        # self.timer.timeout.connect(self.refresh_table)

        # self.timer.start()  
        if auto_update:
            self.selection_model.sessionChanged.connect(self.refresh_table)

    def refresh_editors(self):
        # Iterate through all rows in the column for stint_type
        for row in range(self.table.model().rowCount()):
            index = self.table.model().index(row, 0)  # 0 = stint_type column
            cell_text = str(index.data())

            if cell_text:  # non-empty → open editor
                self.table.openPersistentEditor(index)
            else:  # empty → close editor
                self.table.closePersistentEditor(index)

    def refresh_table(self):
        self.column_count = 0
        if self.table.model():
            column_count = self.table.model().columnCount()
            if self.column_count != column_count:
                self.set_columns()


        if self.table.model() is None:
            # First time
            # self.model = TableModel(self.selection_model, self.table.headers)
            self.table.setModel(self.table_model)

            self.column_count = self.table.model().columnCount()
            self.set_columns()

        else:
            # Update existing model
            self.table_model.update_data()

    def set_columns(self):
        hh = self.table.horizontalHeader()
        hh.setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed) # Driver
        self.table.setColumnWidth(0, 256) 

        hh.setSectionResizeMode(1, QHeaderView.ResizeMode.Fixed) # Driven
        self.table.setColumnWidth(1, 64)

        hh.setSectionResizeMode(2, QHeaderView.ResizeMode.Fixed) # Pit end time
        self.table.setColumnWidth(2, 128)

        hh.setSectionResizeMode(3, QHeaderView.ResizeMode.Fixed) # Tires changed
        self.table.setColumnWidth(3, 96)

        hh.setSectionResizeMode(4, QHeaderView.ResizeMode.Fixed) # Tires left
        self.table.setColumnWidth(4, 96)

        hh.setSectionResizeMode(5, QHeaderView.ResizeMode.Fixed) # Stint time
        self.table.setColumnWidth(5, 128)

        self.table.setMinimumWidth(hh.length() + 100)
        hh.setSectionsMovable(False)
        hh.setCascadingSectionResizes(False)
        hh.setHighlightSections(False)

    def message(self, s):
        self.text.appendPlainText(s)

