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
from PyQt6.QtCore import QProcess, QTimer, Qt
from PyQt6.QtGui import QIcon
from helpers.stinttracker import get_stints, get_sessions, get_events
from helpers import stints_to_table
from .TableModel import TableModel
from .TitleBar import TitleBar

class StintTracker(QWidget):

    def __init__(self):
        super().__init__()

        container = QHBoxLayout(self)

        self.table = QTableView()
        self.table.setAlternatingRowColors(True)
        self.table.headers = [
            "Driver",
            "Driven",
            "Pit end time",
            "Tires changed",
            "Tires left",
            "Stint time"
        ]

        ### REGION - VISUAL ELEMENTS ###

        # Execution button
        self.btn_track = QPushButton("Start tracking")
        self.btn_track.pressed.connect(self.start_process)

        self.btn_stop = QPushButton("Stop tracking")
        self.btn_stop.pressed.connect(self.stop_process)

        # Log output
        self.text = QPlainTextEdit()
        self.text.setReadOnly(True)

        # Events dropdown
        self.events = QComboBox()
        for doc in get_events():
            self.events.addItem(doc["name"], userData=doc["_id"])
        self.events.currentIndexChanged.connect(self.refresh_sessions)

        # Sessions dropdown
        self.sessions = QComboBox()
        for doc in get_sessions(self.events.currentData()):
            self.sessions.addItem(doc["type"], userData=doc["_id"])

        # Tires field
        self.lbl_tires = QLabel("Starting tires: ")
        self.input_tires = QLineEdit("56", parent=self)
        box_tires = QHBoxLayout()
        box_tires.addWidget(self.lbl_tires)
        box_tires.addWidget(self.input_tires)

        ### REGION - LAYOUTS ###
        
        hbox = QHBoxLayout()

        left_vbox = QVBoxLayout()
        left_vbox.addWidget(self.table)
        left_vbox.addWidget(self.text)

        right_vbox = QVBoxLayout()
        right_vbox.setContentsMargins(100,0,100,0)
        right_vbox.addWidget(self.events)
        right_vbox.addWidget(self.sessions)
        right_vbox.addWidget(self.btn_track)
        right_vbox.addWidget(self.btn_stop)
        right_vbox.addLayout(box_tires)
        self.btn_stop.hide()
        right_vbox.addStretch()

        hbox.addLayout(left_vbox)
        hbox.addLayout(right_vbox)

        w = QWidget()
        w.setLayout(hbox)

        container.addWidget(w)

        self.timer = QTimer(self)
        self.timer.setInterval(1000)  # 1 second
        self.timer.timeout.connect(self.refresh_table)

        self.refresh_table()      # initial load
        self.timer.start()  

    def refresh_sessions(self):
        self.sessions.clear()
        for doc in get_sessions(self.events.currentData()):
            self.sessions.addItem(doc["type"], userData=doc["_id"])


    def refresh_table(self):
        stints = list(get_stints(self.sessions.currentData()))
        data = stints_to_table(stints, self.input_tires.text())

        if not hasattr(self, "model"):
            # First time
            self.model = TableModel(data, self.table.headers)
            self.table.setModel(self.model)
            self.table.resizeColumnsToContents()
        else:
            # Update existing model
            self.model.update_data(data)

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
            str(self.sessions.currentData()),
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

