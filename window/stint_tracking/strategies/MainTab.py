from PyQt6.QtWidgets import ( 
        QMainWindow, 
        QTableView, 
        QGridLayout,
        QPushButton, 
        QFrame,
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
from bson import ObjectId
from PyQt6.QtCore import QProcess, QTimer, Qt, QSize, pyqtSignal
from PyQt6.QtGui import QIcon
from helpers.stinttracker import get_stints, get_event
from helpers import stints_to_table, resource_path
from window.models import TableModel
from ...TitleBar import TitleBar
from ...Fonts import FONT, get_fonts
from ...models import NavigationModel, SelectionModel
from ..StintTracker import StintTracker
from helpers.stinttracker import get_sessions, get_events
from helpers.strategies import sanitize_stints, update_strategy, create_strategy

class MainTab(QWidget):
    strategy_created = pyqtSignal(dict)

    def __init__(self, models = {"selection_model": SelectionModel()}):
        super().__init__()


        self.selection_model = models['selection_model']
        self.table_model = models['table_model']
        self.inputs = {}

        layout = QHBoxLayout(self)
        layout.addWidget(self.create_strategy_widget())
        layout.addWidget(self.create_stats())

    def create_strategy_widget(self):
        frame = QFrame()
        frame.setFixedWidth(336)
        layout = QVBoxLayout(frame)

        strategy_name = self.create_row("strategy_name", "Strategy name", "Name to be used in the tab")
        base_event = self.create_row("base_event", "Base event", "Taken from session picker at top", text=self.selection_model.event_name, read_only=True)
        base_session = self.create_row("base_session", "Base session", "Taken from session picker at top", text=self.selection_model.session_name, read_only=True)
        create_btn = self.create_submit_btn()

        layout.addWidget(strategy_name)
        layout.addWidget(base_event)
        layout.addWidget(base_session)
        layout.addWidget(create_btn)
        layout.addStretch()

        return frame

    def create_row(self, id, title, hint, text = "", read_only=False):
        card = QFrame()
        card.setObjectName("SettingStrategy")
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
        input.setFont(font_input)
        input.setReadOnly(read_only)
        self.inputs[id] = input

        main_box.addWidget(title_label)
        main_box.addWidget(hint_label)
        main_box.addWidget(input)

        return card

    def create_submit_btn(self):
        btn = QPushButton("Create strategy")
        btn.setSizePolicy(
            QSizePolicy.Policy.Maximum,  # width adjusts to minimum needed
            QSizePolicy.Policy.Minimum   # height adjusts to fit content
        )
        btn.clicked.connect(self.create_strategy)

        return btn

    def create_strategy(self):
        row_data, tire_data = self.table_model.get_all_data()
        sanitized_data = sanitize_stints(row_data, tire_data)
        strategy = {
            "session_id": ObjectId(self.selection_model.session_id),
            "name": self.inputs['strategy_name'].text(),
            "model_data": sanitized_data
        }
        create_strategy(strategy)
        self.strategy_created.emit(strategy)

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

    def create_stats(self):
        frame = QFrame()
        layout = QGridLayout(frame)

        event = get_event(self.selection_model.event_id)

        layout.addWidget(self.create_stat("Tires available", event['tires']), 0, 0, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(self.create_stat("Race length", event['length']), 1, 0, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        layout.setRowStretch(2, 1)
        
        return frame

    def create_stat(self, header, value):
        frame = QFrame()
        frame.setSizePolicy(
            QSizePolicy.Policy.Maximum,  # width adjusts to minimum needed
            QSizePolicy.Policy.Maximum   # height adjusts to fit content
        )
        layout = QVBoxLayout(frame)
        font_header = get_fonts(FONT.header_input)
        font_value = get_fonts(FONT.text_small)

        lbl_header = QLabel(header)
        lbl_header.setFont(font_header)

        lbl_value = QLabel(value)
        lbl_value.setFont(font_value)

        layout.addWidget(lbl_header)
        layout.addWidget(lbl_value)

        return frame