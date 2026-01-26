from PyQt6.QtWidgets import ( 
        QMainWindow, 
        QTableView, 
        QPushButton, 
        QFrame,
        QCheckBox,
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
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtCore import QProcess, QTimer, Qt, QSize

from ...models import NavigationModel, SelectionModel
from helpers import resource_path
from helpers.stinttracker.races import get_event, get_session, create_event, create_session, get_sessions
from helpers.db.teams import get_team, update_drivers
from ...Fonts import FONT, get_fonts
from helpers.db import events_col, teams_col, sessions_col
from bson import ObjectId
from datetime import datetime

class ConfigOptions(QWidget):
    stint_created = pyqtSignal()

    def __init__(self, models = {"selection_model": SelectionModel()}):
        super().__init__()
        self.selection_model = models['selection_model']
        self.table_model = models['table_model']
        self.event = get_event(self.selection_model.event_id)
        self.session = get_session(self.selection_model.session_id)
        self.selection_model.eventChanged.connect(self.set_labels)
        self.selection_model.sessionChanged.connect(self.set_labels)

        with open(resource_path('styles/config_options.qss'), 'r') as f:
            style = f.read()

        self.setStyleSheet(style)
        self.inputs = {}
        font_cb = get_fonts(FONT.header_input_hint)

        frame = QFrame()
        frame.setObjectName("ConfigOptions")
        frame.setFixedWidth(272)

        root_widget_layout = QVBoxLayout(self)   
        root_widget_layout.addWidget(frame)

        self.edit_btn = QPushButton("Edit")
        self.save_btn = QPushButton("Save")
        self.clone_btn = QPushButton("Clone event")
        self.create_session_btn = QPushButton("New session")

        self.start_btn = QPushButton("Start tracking")
        self.stop_btn = QPushButton("Stop tracking")

        self.practice_cb = QCheckBox(text="Practice")
        self.lbl_return_to_grg = QLabel("Please return to garage!")
        self.practice_cb.setFont(font_cb)
        self.lbl_return_to_grg.setFont(font_cb)

        btn_layout = QHBoxLayout()
        btn_tracking_layout = QVBoxLayout()
        btn_tracking_layout.setSpacing(8)

        btn_layout_save_clone = QVBoxLayout()
        btn_layout_save_clone.addWidget(self.edit_btn, alignment=Qt.AlignmentFlag.AlignTop)
        btn_layout_save_clone.addWidget(self.save_btn, alignment=Qt.AlignmentFlag.AlignTop)
        btn_layout_save_clone.addWidget(self.clone_btn, alignment=Qt.AlignmentFlag.AlignTop)
        btn_layout_save_clone.addWidget(self.create_session_btn, alignment=Qt.AlignmentFlag.AlignTop)

        btn_layout.addLayout(btn_layout_save_clone)

        btn_tracking_layout.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignTop)
        btn_tracking_layout.addWidget(self.stop_btn, alignment=Qt.AlignmentFlag.AlignTop)
        btn_tracking_layout.addWidget(self.practice_cb, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        btn_tracking_layout.addWidget(self.lbl_return_to_grg, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        btn_tracking_layout.addStretch()
        self.lbl_return_to_grg.hide()
        btn_layout.addLayout(btn_tracking_layout)
        btn_layout.setSpacing(8)

        self.edit_btn.clicked.connect(self.toggle_edit)
        self.save_btn.clicked.connect(self.toggle_edit)
        self.save_btn.clicked.connect(self.save_config)
        self.clone_btn.clicked.connect(self.clone_event)
        self.create_session_btn.clicked.connect(self.create_session)

        self.stop_btn.clicked.connect(self.toggle_track)
        self.start_btn.clicked.connect(self.toggle_track)

        # Root vertical container
        root_layout = QVBoxLayout(frame)
        root_layout.setContentsMargins(0,0,16,0)
        root_layout.setSpacing(32)
        root_layout.addWidget(
            self.create_row("event_name", "Event name", "Name of the endurance race", 0, self.event.get('name'))
            )
        root_layout.addWidget(
            self.create_row("session_name", "Session name", "Name of this specific session", 0, self.session.get('name'))
            )
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

    def set_labels(self):
        self.event = get_event(self.selection_model.event_id)
        self.session = get_session(self.selection_model.session_id)

        self.inputs['event_name'].setText(self.event['name'])
        if not self.session:
            self.session = list(get_sessions(self.event['_id']))[-1]
            self.selection_model.set_session(self.session['_id'], self.session['name'])

        self.inputs['session_name'].setText(self.session['name'])
        self.inputs['tires'].setText(self.event['tires'])
        self.inputs['length'].setText(self.event['length'])

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
        
        if input_width:
            input.setFixedWidth(input_width)

        input.setSizePolicy(
            QSizePolicy.Policy.Expanding,  # width adjusts to minimum needed
            QSizePolicy.Policy.Minimum   # height adjusts to fit content
        )
        
        input.setFixedHeight(40)
        input.setFont(font_input)
        input.setReadOnly(True)
        self.inputs[id] = input

        main_box.addWidget(title_label)
        main_box.addWidget(hint_label)
        if input_width:
            input.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTop)
            main_box.addWidget(input, alignment=Qt.AlignmentFlag.AlignRight)
        else:
            input.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
            main_box.addWidget(input, stretch=1)


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
            self.clone_btn.hide()
            self.save_btn.show()
            for child in self.findChildren(QLineEdit):
                child.setReadOnly(False)
                child.setStyleSheet(
                    """background-color: transparent;
                    """
                )
        else:
            self.save_btn.hide()
            self.clone_btn.show()
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
        self.p.readyReadStandardOutput.connect(self.handle_stdout)
        self.p.readyReadStandardError.connect(self.handle_stderr)
        is_practice = self.practice_cb.isChecked()
        process_args = [
            '-u', 
            'update_stint.py', 
            '--session-id', str(self.selection_model.session_id),
            '--drivers', *self.drivers
            ]
        if is_practice:
            process_args.append('--practice')

        self.p.start("python3", process_args)
        print('Starting process: python3 ', process_args)

    def handle_stderr(self):
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        print(stderr)

    def handle_stdout(self):
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        print(stdout)
        if stdout.startswith('__'):
            self.handle_output(stdout)

    def handle_output(self, stdout):

        args = stdout.split(':')
        process = args[1].strip()
        msg = args[2].strip()

        if stdout.startswith('__event__'):
            if process == 'stint_tracker':
                if msg == 'stint_created':
                    self.stint_created.emit()
        if stdout.startswith('__info__'):
            if process == 'stint_tracker':
                if msg == 'return_to_garage':
                    self.lbl_return_to_grg.show()
                if msg == 'player_in_garage':
                    self.lbl_return_to_grg.hide()

    def save_config(self):
        event_query = { "_id": ObjectId(self.selection_model.event_id) }
        session_query = { "_id": ObjectId(self.selection_model.session_id) }

        tires = self.inputs['tires'].text()
        length = self.inputs['length'].text()
        event_name = self.inputs['event_name'].text()
        session_name = self.inputs['session_name'].text()
        event_doc = { "$set":{
            "name": event_name,
            "tires": tires,
            "length": length
        }}
        session_doc = { "$set":{
            "name": session_name,
        }}

        events_col.update_one(event_query, event_doc)
        sessions_col.update_one(session_query, session_doc)
        self.table_model.update_data()

        drivers = []
        for _, line_edit in self.driver_inputs.items():
            drivers.append(line_edit.text())

        update_drivers(self.team['_id'], drivers)

    def clone_event(self):
        event = get_event(self.selection_model.event_id)
        del event['_id']
        event['name'] = event['name'] + " - Clone"
        event_created  = create_event(event)

        session = {
            "race_id": event_created.inserted_id,
            "name": "practice"
        }

        session_created = create_session(session)
        event = get_event(event_created.inserted_id)
        session = get_session(session_created.inserted_id)

        self.selection_model.set_event(event['_id'], event['name'])
        self.selection_model.set_session(session['_id'], session['name'])

    def create_session(self):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_name = "Practice - " + now

        session_doc = {
            "race_id": ObjectId(self.selection_model.event_id),
            "name": session_name
        }
        session = create_session(session_doc)
        self.selection_model.set_session(session.inserted_id, session_doc['name'])
