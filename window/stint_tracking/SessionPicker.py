from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QComboBox, 
    QWidget,
    QPushButton,
    QFrame,
    QLineEdit,
    QSizePolicy
)
from PyQt6.QtCore import QSize, Qt 
from helpers.stinttracker import get_sessions, get_events
from helpers import resource_path
from window.Fonts import FONT, get_fonts

class SessionPicker(QWidget):
    def __init__(self, selection_model):
        super().__init__()
        self.selection_model = selection_model

        with open(resource_path('styles/session_picker.qss'), 'r') as f:
            style = f.read()

        self.setObjectName("StintSelection")
        self.setStyleSheet(style)
        self.setFixedHeight(112)

        frame = QFrame()
        frame.setObjectName("ComboBoxes")

        root_widget_layout = QVBoxLayout(self)   
        root_widget_layout.addWidget(frame)

        # Root horizontal container
        root_layout = QHBoxLayout(frame)
        # root_layout.setContentsMargins(24, 32, 24, 24)  # top padding emphasized
        root_layout.setSpacing(16)
        root_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Events dropdown
        self.events = QComboBox()
        for doc in get_events():
            self.events.addItem(doc["name"], userData=doc["_id"])

        # Sessions dropdown
        self.sessions = QComboBox()
        for doc in get_sessions(self.events.currentData()):
            self.sessions.addItem(doc["type"], userData=doc["_id"])
        self.events.currentIndexChanged.connect(self.on_event_changed)
        self.sessions.currentIndexChanged.connect(self.on_session_changed)

        self.on_event_changed() # Initial Load

        # Create cards
        event_card = self._create_card(
            label_text="Event",
            box=self.events
        )

        session_card = self._create_card(
            label_text="Session",
            box=self.sessions
        )

        root_layout.addWidget(event_card)
        root_layout.addWidget(session_card)

    def _create_card(self, label_text: str, box: QComboBox) -> QFrame:
          card = QFrame()
          card.setObjectName("InputCard")
          card.setFixedSize(512, 80)

          layout = QVBoxLayout(card)
          layout.setContentsMargins(0, 0, 16, 32)
          layout.setSpacing(4)
          layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

          # Left label (bold)
          font_header_input = get_fonts(FONT.header_input)
          label = QLabel(label_text)
          label.setObjectName("CardLabel")
          label.setFont(font_header_input)

          # Right dropdown
          input_field = box
          input_field.setObjectName("ComboBox")
          input_field.setFixedHeight(32)

          layout.addWidget(label)
          layout.addWidget(input_field, stretch=1)

          return card

    # Event changed
    def on_event_changed(self):
        event_id = self.events.currentData()
        self.selection_model.set_event(event_id)

        # Repopulate sessions safely
        self.sessions.blockSignals(True)
        self.sessions.clear()
        for doc in get_sessions(event_id):
            self.sessions.addItem(doc["type"], userData=doc["_id"])
        self.sessions.blockSignals(False)

        # Set model to first session by default
        if self.sessions.count() > 0:
            self.selection_model.set_session(self.sessions.currentData())
        else:
            self.selection_model.set_session(None)

    # Session changed
    def on_session_changed(self):
        self.selection_model.set_session(self.sessions.currentData())