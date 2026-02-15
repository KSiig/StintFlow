from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel,
    QWidget, QFrame, QGraphicsDropShadowEffect, QSizePolicy, 
    QPushButton, QHBoxLayout
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

from core.utilities import resource_path
from core.errors import log
from ui.utilities import FONT, get_fonts, load_icon

class PopUp(QDialog):

    def __init__(self, title, message, buttons=None, type="info", parent=None):
        super().__init__(parent)
        self._setup_styles()

        # Icon map is now accessible throughout the instance
        self._icon_map = {
            "info": ("resources/icons/popup/info.svg", "#3b82f6"),
            "error": ("resources/icons/popup/circle-x.svg", "#ef4444"),
            "warning": ("resources/icons/popup/triangle-alert.svg", "#f59e0b"),
            "critical": ("resources/icons/popup/circle-alert.svg", "#dc2626")
        }
        icon_path, self._icon_color = self._icon_map.get(type, ("resources/icons/popup/info.svg", "#3b82f6"))
        self.setFixedSize(510, 248)  # Set a default size for the popup

        # 1. Make the actual Dialog window invisible/transparent
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Dialog)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        # 2. The Main Layout (this holds the shadow-space)
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(20, 20, 20, 20) # Space for shadow

        # 3. The Content Frame (The "Visual" Dialog)
        self.container = QFrame()
        self.container.setObjectName("ContentFrame")
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(28, 28, 28, 28)

        # Set the left border to match the icon color
        self.container.setStyleSheet(f"""
            QFrame#ContentFrame {{
                background-color: white;
                border-radius: 8px;
                border-left: 2px solid {self._icon_color};
            }}
        """)

        # 4. Add UI Elements to the container_layout in order: icon, title, message, button
        # --- Icon (SVG, centered, type-based) ---
        icon_frame = QFrame()
        icon_frame.setObjectName("IconFrame")
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0) 
        icon_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.icon_label = QLabel()
        self.icon_label.setFixedSize(32, 32)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.icon_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self._set_icon(type)
        icon_layout.addWidget(self.icon_label)
        self.container_layout.addWidget(icon_frame)

        self.container_layout.addSpacing(8)  # Space between icon and title

        # --- Title ---
        self.title_label = QLabel(title)
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.title_label.setFont(get_fonts(FONT.dialog_header))
        self.container_layout.addWidget(self.title_label)

        # --- Message ---
        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        self.label.setFont(get_fonts(FONT.dialog_msg))
        self.container_layout.addWidget(self.label)

        # --- Button(s) ---
        if buttons is None:
            buttons = ["Ok"]
        button_row = QWidget()
        button_row.setObjectName("ButtonRow")
        button_layout = QHBoxLayout(button_row)
        button_layout.setContentsMargins(0, 16, 0, 0)
        button_layout.setSpacing(16)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        for btn_text in buttons:
            _, color = self._icon_map.get(type, ("", "#3b82f6"))
            btn = QPushButton(btn_text)
            btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                border-radius: 4px;
                padding: 6px 12px;
                color: white;
            }}
        """)
            btn.clicked.connect(lambda _, b=btn_text: self._handle_click(b))
            button_layout.addWidget(btn)
        self.container_layout.addWidget(button_row)

        # Add container to main layout
        self.main_layout.addWidget(self.container)

        # 5. Apply the Shadow to the container
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(25)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(4)
        self.shadow.setColor(QColor(0, 0, 0, 180))
        self.container.setGraphicsEffect(self.shadow)

        self.setMinimumWidth(390) # Adjusted for the 20px margins

    def _set_icon(self, type: str):
        """Set the icon pixmap and color based on the popup type."""
        icon_path, color = self._icon_map.get(type, ("resources/icons/popup/info.svg", "#3b82f6"))
        icon_pixmap = load_icon(icon_path, size=32, color=color)
        self.icon_label.setPixmap(icon_pixmap)

    def _setup_styles(self) -> None:
        """Load and apply popup stylesheet."""
        try:
            with open(resource_path('resources/styles/popup.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            log('WARNING', 'Popup stylesheet not found', 
                category='popup', action='load_stylesheet')

    def showEvent(self, event):
        super().showEvent(event)
        QTimer.singleShot(0, self._center_on_parent)

    def _center_on_parent(self):
        self.adjustSize()
        parent = self.parent()
        if parent:
            window = parent.window()
            center_point = window.frameGeometry().center()
        else:
            center_point = self.screen().availableGeometry().center()

        rect = self.frameGeometry()
        rect.moveCenter(center_point)
        self.move(rect.topLeft())

    def _handle_click(self, button_text: str):
        self.clicked_button = button_text
        self.accept()