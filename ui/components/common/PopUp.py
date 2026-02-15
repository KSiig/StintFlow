from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QDialogButtonBox, 
    QWidget, QFrame, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor

from core.utilities import resource_path
from core.errors import log

class PopUp(QDialog):
    def __init__(self, title, message, buttons=None, icon_type="info", parent=None):
        super().__init__(parent)
        self._setup_styles()

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
        self.container_layout.setContentsMargins(15, 15, 15, 15)
        
        # Apply your background colors to the container instead of the dialog
        self._apply_container_style(icon_type)

        # 4. Add UI Elements to the container_layout
        self.label = QLabel(message)
        self.label.setWordWrap(True)
        self.container_layout.addWidget(self.label)

        if buttons is None: buttons = ["Ok"]
        self.button_box = QDialogButtonBox()
        for btn_text in buttons:
            button = self.button_box.addButton(btn_text, QDialogButtonBox.ButtonRole.AcceptRole)
            button.clicked.connect(lambda _, b=btn_text: self._handle_click(b))
        self.container_layout.addWidget(self.button_box)

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

    def _setup_styles(self) -> None:
        """Load and apply popup stylesheet."""
        try:
            with open(resource_path('resources/styles/popup.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            log('WARNING', 'Popup stylesheet not found', 
                category='popup', action='load_stylesheet')

    def _apply_container_style(self, icon_type: str):
        colors = {
            "warning": "#ffe082",
            "error": "#ff8a80",
            "info": "#bbdefb"
        }
        bg_color = colors.get(icon_type, "#e8f4fd")
        
        # We style the container, giving it a border and radius
        self.container.setStyleSheet(f"""
            QFrame#ContentFrame {{
                background-color: {bg_color};
                border: 1px solid rgba(0,0,0,0.1);
                border-radius: 8px;
            }}
            QLabel {{ color: #333; font-size: 14px; }}
        """)

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