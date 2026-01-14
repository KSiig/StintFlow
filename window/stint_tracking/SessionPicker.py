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
from helpers.stinttracker.races import get_event, get_session
from helpers import resource_path
from window.Fonts import FONT, get_fonts
from ..models import NavigationModel, SelectionModel
from bson import ObjectId
from bson.errors import InvalidId

class SessionPicker(QWidget):
    def __init__(self, models = {"selection_model": SelectionModel()}):
        super().__init__()
        self.selection_model = models['selection_model']

        with open(resource_path('styles/session_picker.qss'), 'r') as f:
            style = f.read()

        self.setObjectName("StintSelection")
        self.setStyleSheet(style)
        self.setSizePolicy(
            QSizePolicy.Policy.Minimum,  # width adjusts to minimum needed
            QSizePolicy.Policy.Maximum   # height adjusts to fit content
        )

        frame = QFrame()
        frame.setObjectName("ComboBoxes")
        frame.setSizePolicy(
            QSizePolicy.Policy.Minimum,  # width adjusts to minimum needed
            QSizePolicy.Policy.Fixed   # height adjusts to fit content
        )

        root_widget_layout = QVBoxLayout(self)   
        root_widget_layout.setContentsMargins(0,0,8,0)
        root_widget_layout.addWidget(frame)

        # Root horizontal container
        root_layout = QVBoxLayout(frame)
        root_layout.setContentsMargins(0,0,0,0)  # top padding emphasized
        root_layout.setSpacing(16)
        root_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Events dropdown
        self.events = QComboBox()
        self.events.setEditable = True
        for doc in get_events():
            self.events.addItem(doc["name"], userData=str(doc["_id"]))

        # Sessions dropdown
        self.sessions = QComboBox()
        for doc in get_sessions(self.events.currentData()):
            self.sessions.addItem(doc["name"], userData=str(doc["_id"]))
        self.events.currentIndexChanged.connect(self.on_event_changed)
        self.sessions.currentIndexChanged.connect(self.on_session_changed)

        event_id = self.selection_model.event_id
        session_id = self.selection_model.session_id
        event_index = self.events.findData(str(event_id))
        session_index = self.sessions.findData(str(session_id))

        if event_index >= 0:
            self.events.setCurrentIndex(event_index)

        self.on_event_changed() # Initial Load

        if event_index >= 0:
            self.sessions.setCurrentIndex(session_index)
        
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
        #   card.setFixedSize(512, 80)
          card.setSizePolicy(
              QSizePolicy.Policy.Minimum,  # width adjusts to minimum needed
              QSizePolicy.Policy.Fixed   # height adjusts to fit content
          )

          layout = QVBoxLayout(card)
          layout.setContentsMargins(0, 0, 0, 0)
          layout.setSpacing(4)
          layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

          font_lbl = get_fonts(FONT.header_input_hint)
          label = QLabel(label_text)
          label.setObjectName("CardLabel")
          label.setFont(font_lbl)

          # Right dropdown
          input_field = box
          input_field.setObjectName("ComboBox")
          input_field.setFont(font_lbl)
          input_field.setSizePolicy(
              QSizePolicy.Policy.Minimum,  # width adjusts to minimum needed
              QSizePolicy.Policy.Fixed   # height adjusts to fit content
          )

          layout.addWidget(label)
          layout.addWidget(input_field, stretch=1)

          return card

    # Event changed
    def on_event_changed(self, event_id = "", event_name = ""):

        event_id = self.events.currentData()
        event_name = self.events.currentText()
        self.selection_model.set_event(event_id, event_name)

        # Repopulate sessions safely
        self.sessions.blockSignals(True)
        self.sessions.clear()
        for doc in get_sessions(event_id):
            self.sessions.addItem(doc["name"], userData=str(doc["_id"]))
        self.sessions.blockSignals(False)

        # Set model to first session by default
        if self.sessions.count() > 0:
            self.selection_model.set_session(self.sessions.currentData(), self.sessions.currentText())
        else:
            self.selection_model.set_session(None)

    # Session changed
    def on_session_changed(self):
        self.selection_model.set_session(self.sessions.currentData(), self.sessions.currentText())

    def update_event_selection(self, event_id, event_name):
        self.events.blockSignals(True)
        for i in range(self.events.count()):
            if self.events.itemData(i) == event_id:
                self.events.setItemText(i, event_name)
                self.events.setCurrentIndex(i)
                return

         # Force Qt to update displayed text
        self.events.setEditable(True)
        self.events.setCurrentText(event_name)
        self.events.setEditable(False)
        self.events.setCurrentIndex(self.events.count() - 1)

        self.on_event_changed()
        self.events.blockSignals(False)

    def update_session_selection(self, session_id, session_name):
        for i in range(self.sessions.count()):
            if self.events.itemData(i) == session_id:
                self.events.setCurrentIndex(i)
                return
        print()


    def reload(self, selected_event_id=None, selected_session_id=None):
        """
        Refresh events and sessions combo boxes.
        Optionally select a specific event/session.
        """
        self.events.blockSignals(True)
        self.sessions.blockSignals(True)

        # --- Refresh events ---
        self.events.clear()
        for doc in get_events():
            self.events.addItem(doc["name"], userData=str(doc["_id"]))

        # Select event
        if selected_event_id:
            index = self.events.findData(str(selected_event_id))
            if index >= 0:
                self.events.setCurrentIndex(index)
        else:
            # Keep current selection if possible
            index = self.events.findData(str(self.selection_model.event_id))
            if index >= 0:
                self.events.setCurrentIndex(index)

        # --- Refresh sessions ---
        event_id = self.events.currentData()
        self.sessions.clear()
        for doc in get_sessions(event_id):
            self.sessions.addItem(doc["name"], userData=str(doc["_id"]))

        # Select session
        if selected_session_id:
            index = self.sessions.findData(str(selected_session_id))
            if index >= 0:
                self.sessions.setCurrentIndex(index)
        else:
            index = self.sessions.findData(str(self.selection_model.session_id))
            if index >= 0:
                self.sessions.setCurrentIndex(index)

        # Update selection model to match combobox
        self.selection_model.set_event(self.events.currentData(), self.events.currentText())
        self.selection_model.set_session(self.sessions.currentData(), self.sessions.currentText())

        self.sessions.blockSignals(False)
        self.events.blockSignals(False)