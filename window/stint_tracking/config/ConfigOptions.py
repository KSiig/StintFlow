from PyQt6.QtWidgets import ( 
        QMainWindow, 
        QTableView, 
        QPushButton, 
        QFrame,
        QWidget, 
        QVBoxLayout, 
        QSpacerItem,
        QSizePolicy,
        QHBoxLayout, 
        QPlainTextEdit, 
        QComboBox, 
        QLineEdit, 
        QLabel
    )
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QProcess, QTimer, Qt, QSize

from ...models import NavigationModel, SelectionModel
from helpers import resource_path
from helpers.stinttracker.races import get_event
from helpers.db.teams import get_team, update_drivers
from ...Fonts import FONT, get_fonts
from helpers.db import events_col, teams_col
from bson import ObjectId

class ConfigOptions(QWidget):
    def __init__(self, models = {"selection_model": SelectionModel()}):
        super().__init__()
        self.selection_model = models['selection_model']
        self.table_model = models['table_model']
        self.event = get_event(self.selection_model.event_id)

        with open(resource_path('styles/config_options.qss'), 'r') as f:
            style = f.read()

        self.setStyleSheet(style)
        self.inputs = {}

        frame = QFrame()
        frame.setObjectName("ConfigOptions")
        frame.setFixedWidth(272)

        root_widget_layout = QVBoxLayout(self)   
        root_widget_layout.addWidget(frame)

        self.edit_btn = QPushButton("Edit")
        self.save_btn = QPushButton("Save")
        self.start_btn = QPushButton("Start tracking")
        self.stop_btn = QPushButton("Stop tracking")

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.edit_btn)
        btn_layout.addWidget(self.save_btn)
        btn_layout.addWidget(self.start_btn)
        btn_layout.addWidget(self.stop_btn)
        btn_layout.setSpacing(8)

        self.edit_btn.clicked.connect(self.toggle_edit)
        self.save_btn.clicked.connect(self.toggle_edit)
        self.save_btn.clicked.connect(self.save_config)

        self.stop_btn.clicked.connect(self.toggle_track)
        self.start_btn.clicked.connect(self.toggle_track)

        # Root vertical container
        root_layout = QVBoxLayout(frame)
        root_layout.setContentsMargins(0,0,16,0)
        root_layout.setSpacing(32)
        root_layout.addWidget(
            self.create_row("tires", "Starting tires", "How many tires at start of event", 54, self.event.get('tires'))
            )
        root_layout.addWidget(
            self.create_row("length", "Race length", "Hours and minutes of the race (HH:MM:SS)", 96, self.event.get('length'))
            )
        root_layout.addWidget(self.create_team_config())
        root_layout.addLayout(btn_layout)
        self.save_btn.hide()
        self.stop_btn.hide()
        root_layout.addStretch()

    def create_labels(self, title, hint):
        font_title = get_fonts(FONT.header_input)
        font_hint = get_fonts(FONT.header_input_hint)

        # Title
        title_label = QLabel(title)
        title_label.setObjectName("SettingTitle")
        title_label.setFont(font_title)
        title_label.setContentsMargins(0,0,0,0)
        # title_label.setFixedHeight(40)
        title_label.setSizePolicy(
            QSizePolicy.Policy.Minimum,  # width adjusts to minimum needed
            QSizePolicy.Policy.Minimum   # height adjusts to fit content
        )
        title_label.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Tooltip
        hint_label = QLabel(hint)
        hint_label.setObjectName("SettingHint")
        hint_label.setFont(font_hint)
        # hint_label.setFixedHeight(40)
        hint_label.setSizePolicy(
            QSizePolicy.Policy.Minimum,  # width adjusts to minimum needed
            QSizePolicy.Policy.Minimum   # height adjusts to fit content
        )
        hint_label.setAlignment(Qt.AlignmentFlag.AlignTop)
        hint_label.setContentsMargins(0,0,0,8)

        return title_label, hint_label

    def create_row(self, id, title, hint, input_width = 336, text = ""):
        card = QFrame()
        card.setObjectName("Setting")
        card.setSizePolicy(
            QSizePolicy.Policy.Minimum,  # width adjusts to minimum needed
            QSizePolicy.Policy.Minimum   # height adjusts to fit content
        )
        card.setContentsMargins(0,0,0,0)

        main_box = QVBoxLayout(card)
        main_box.setContentsMargins(0,0,0,0)
        main_box.setSpacing(0)

        font_input = get_fonts(FONT.text_small)

        title_label, hint_label = self.create_labels(title, hint)

        # Input box
        input = QLineEdit(text)
        input.setFixedWidth(input_width)
        input.setFixedHeight(40)
        input.setFont(font_input)
        input.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
        input.setReadOnly(True)
        self.inputs[id] = input

        main_box.addWidget(title_label)
        main_box.addWidget(hint_label)
        main_box.addWidget(input, alignment=Qt.AlignmentFlag.AlignRight)

        return card

    def create_team_config(self):
        card = QFrame()
        card.setObjectName("DriverNames")
        card.setSizePolicy(
            QSizePolicy.Policy.Minimum,  # width adjusts to minimum needed
            QSizePolicy.Policy.Minimum   # height adjusts to fit content
        )
        card.setContentsMargins(0,0,0,0)

        title_label, hint_label = self.create_labels("Driver names", "Names as written in the game")

        main_box = QVBoxLayout(card)
        main_box.setContentsMargins(0,0,0,0)
        main_box.setSpacing(0)
        main_box.addWidget(title_label)
        main_box.addWidget(hint_label)

        driver_box = QVBoxLayout()
        driver_box.setSpacing(8)
        main_box.addLayout(driver_box)

        self.team = get_team()
        self.drivers = self.team['drivers']
        self.driver_inputs = {}

        # Create a QLineEdit for each driver
        for driver in self.drivers:
            line_edit = QLineEdit(driver)
            line_edit.setReadOnly(True)
            driver_box.addWidget(line_edit)
            self.driver_inputs[driver] = line_edit  # store reference

        return card

    def toggle_edit(self):
        # Edit is clicked
        if self.save_btn.isHidden():
            self.edit_btn.hide()
            self.save_btn.show()
            for child in self.findChildren(QLineEdit):
                child.setReadOnly(False)
                child.setStyleSheet(
                    """background-color: transparent;
                    """
                )
        else:
            self.save_btn.hide()
            self.edit_btn.show()
            for child in self.findChildren(QLineEdit):
                child.setReadOnly(True)
                child.setStyleSheet(
                    """background-color: #EBEBE4;
                    """
                )

    def toggle_track(self):
        # Start is clicked
        if self.stop_btn.isHidden():
            self.start_btn.hide()
            self.stop_btn.show()
            self.start_process()
        else:
            self.stop_btn.hide()
            self.start_btn.show()
            self.p.kill()

    def start_process(self):
        # We'll run our process here.
        self.p = QProcess()
        # self.p.readyReadStandardOutput.connect(self.handle_stdout)
        # self.p.readyReadStandardError.connect(self.handle_stderr)
        process_args = [
            '-u', 
            'update_stint.py', 
            str(self.selection_model.session_id),
            ','.join(self.drivers)
            ]
        self.p.start("python3", process_args)
        print('Starting process: python3 ', process_args)

    def save_config(self):
        query = { "_id": ObjectId(self.selection_model.event_id) }

        tires = self.inputs['tires'].text()
        length = self.inputs['length'].text()
        doc = { "$set":{
            "tires": tires,
            "length": length
        }}

        events_col.update_one(query, doc)
        self.table_model.update_data()

        drivers = []
        for _, line_edit in self.driver_inputs.items():
            drivers.append(line_edit.text())

        update_drivers(self.team['_id'], drivers)
