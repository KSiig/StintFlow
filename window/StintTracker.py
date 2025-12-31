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
        QAbstractItemView
    )
from PyQt6.QtCore import QProcess, QTimer, Qt, QSize
from PyQt6.QtGui import QIcon
from helpers.stinttracker import get_stints, get_event
from helpers import stints_to_table, resource_path
from window.stint_tracking import TableModel
from .TitleBar import TitleBar
from .Fonts import FONT, get_fonts

class StintTracker(QWidget):

    def __init__(self, selection_model, focus = False):
        super().__init__()

        self.selection_model = selection_model

        with open(resource_path('styles/stint_tracker.qss'), 'r') as f:
            style = f.read()

        self.setStyleSheet(style)

        container = QHBoxLayout(self)

        font_small_text = get_fonts(FONT.text_small)
        font_table_header = get_fonts(FONT.header_table)
        self.table = QTableView(self)
        self.table.setShowGrid(False)
        self.table.headers = [
            "Driver",
            "Driven",
            "Pit end time",
            "Tires changed",
            "Tires left",
            "Stint time"
        ]
        if not focus:
            self.table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
            self.table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.refresh_table()      # initial load

        vh = self.table.verticalHeader()
        vh.setFixedWidth(80)
        vh.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        vh.setFont(font_small_text)

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
        
        self.table.setFont(font_small_text)
        self.table.setObjectName("StintsTable")

        ### REGION - VISUAL ELEMENTS ###

        # Execution button
        # self.btn_track = QPushButton("Start tracking")
        # self.btn_track.pressed.connect(self.start_process)

        # self.btn_stop = QPushButton("Stop tracking")
        # self.btn_stop.pressed.connect(self.stop_process)


        # Tires field
        # self.lbl_tires = QLabel("Starting tires: ")
        # self.input_tires = QLineEdit("56", parent=self)
        # box_tires = QHBoxLayout()
        # box_tires.addWidget(self.lbl_tires)
        # box_tires.addWidget(self.input_tires)

        ### REGION - LAYOUTS ###
        
        container.addWidget(self.table)

        self.timer = QTimer(self)
        self.timer.setInterval(5000)  # 1 second
        self.timer.timeout.connect(self.refresh_table)

        self.timer.start()  
        self.selection_model.sessionChanged.connect(self.refresh_table)

    def refresh_table(self):
        self.column_count = 0
        if self.table.model():
            column_count = self.table.model().columnCount()
            if self.column_count != column_count:
                self.set_columns()

        event = get_event(self.selection_model.event_id)
        if event:
            tires = str(event['tires'])
        else:
            tires = "0"
        
        stints = list(get_stints(self.selection_model.session_id))
        data = stints_to_table(stints, tires)

        if not hasattr(self, "model"):
            # First time
            self.model = TableModel(data, self.table.headers)
            self.table.setModel(self.model)
            self.table.resizeColumnsToContents()

            self.column_count = self.table.model().columnCount()
            self.set_columns()

        else:
            # Update existing model
            self.model.update_data(data)

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

    def start_process(self):
        # We'll run our process here.
        print('Starting process')
        self.btn_track.hide()
        self.btn_stop.show()
        self.p = QProcess()
        self.p.readyReadStandardOutput.connect(self.handle_stdout)
        self.p.readyReadStandardError.connect(self.handle_stderr)
        self.p.start("python3", [
            '-u', 
            'update_stint.py', 
            str(self.selection_model.session_id),
            "Kasper Siig"
            ])

    def stop_process(self):
        self.btn_stop.hide()
        self.btn_track.show()
        self.p.kill()

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self.message(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        self.message(stdout)

    def message(self, s):
        self.text.appendPlainText(s)

