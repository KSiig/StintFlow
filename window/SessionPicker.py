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
)
from PyQt6.QtCore import QSize, Qt
from helpers.stinttracker import get_sessions, get_events
from helpers import resource_path
from .Fonts import FONT, get_fonts

class SessionPicker(QWidget):
      def __init__(self):
        super().__init__()

        # Root horizontal container
        root_layout = QHBoxLayout(self)
        # root_layout.setContentsMargins(24, 32, 24, 24)  # top padding emphasized
        root_layout.setSpacing(16)
        root_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)

        # Events dropdown
        self.events = QComboBox()
        for doc in get_events():
            self.events.addItem(doc["name"], userData=doc["_id"])
        # self.events.currentIndexChanged.connect(self.refresh_sessions)

        # Sessions dropdown
        self.sessions = QComboBox()
        for doc in get_sessions(self.events.currentData()):
            self.sessions.addItem(doc["type"], userData=doc["_id"])

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
        with open(resource_path('styles/session_picker.qss'), 'r') as f:
            style = f.read()

        self.setStyleSheet(style)

      def _create_card(self, label_text: str, box: QComboBox) -> QFrame:
          card = QFrame()
          card.setObjectName("InputCard")
          card.setFixedHeight(64)

          layout = QHBoxLayout(card)
          layout.setContentsMargins(16, 12, 16, 12)
          layout.setSpacing(12)
          layout.setAlignment(Qt.AlignmentFlag.AlignVCenter)

          # Left label (bold)
          font_small_text = get_fonts(FONT.small_text)
          label = QLabel(label_text)
          label.setObjectName("CardLabel")
          label.setFont(font_small_text)

          # Right dropdown
          input_field = box
          input_field.setObjectName("ComboBox")

          layout.addWidget(label)
          layout.addWidget(input_field, stretch=1)

          return card
