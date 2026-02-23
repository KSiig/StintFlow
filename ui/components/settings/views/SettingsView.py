"""
Settings view for application configuration.

Provides UI for MongoDB credentials and other future settings.
"""

import os

from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame
)

from ui.models import ModelContainer
from ui.utilities import get_fonts, FONT
from core.utilities import load_user_settings, save_user_settings
from core.errors import log, log_exception
from core.utilities import resource_path
from ui.components.common import PopUp


class SettingsView(QWidget):
    """
    Application settings view.

    Shows MongoDB connection settings and persists them locally.
    """

    def __init__(self, models: ModelContainer = None) -> None:
        super().__init__()
        self.models = models
        self.inputs: dict[str, QLineEdit] = {}
        self.status_label: QLabel | None = None

        self._setup_styles()
        self._setup_ui()
        self._load_settings()

    def _setup_styles(self) -> None:
        """Load and apply Settings view stylesheet."""
        try:
            with open(resource_path('resources/styles/settings.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError as e:
            log_exception(e, 'Settings menu stylesheet not found', 
                         category='ui', action='load_stylesheet')

    def _setup_ui(self) -> None:
        """Build the settings UI layout."""
        frame = QFrame()
        frame.setObjectName('SettingsFrame')
        frame.setFixedWidth(512)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(frame)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        mongo_frame = QFrame()
        mongo_frame.setObjectName('MongoFrame')
        mongo_layout = QVBoxLayout(mongo_frame)
        mongo_layout.setContentsMargins(0, 0, 0, 0)
        mongo_layout.setSpacing(12)

        mongo_title = QLabel('MongoDB')
        mongo_title.setFont(get_fonts(FONT.header_nav))
        mongo_layout.addWidget(mongo_title)

        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(8)
        form_layout.setHorizontalSpacing(24)

        self._add_input(form_layout, 'Connection string', 'uri', 'mongodb+srv://...')
        self._add_input(form_layout, 'Host', 'host', 'localhost:27017')
        self._add_input(form_layout, 'Database', 'database', 'stintflow')
        self._add_input(form_layout, 'Username', 'username', '')
        self._add_input(form_layout, 'Password', 'password', '', is_password=True)
        self._add_input(form_layout, 'Auth source', 'auth_source', 'admin')

        mongo_layout.addLayout(form_layout)
        layout.addWidget(mongo_frame)

        hint = QLabel('Connection string overrides host and credentials when set.')
        hint.setFont(get_fonts(FONT.header_input_hint))
        layout.addWidget(hint)

        self.status_label = QLabel('')
        self.status_label.setFont(get_fonts(FONT.header_input_hint))
        layout.addWidget(self.status_label)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(8)

        save_button = QPushButton('Save')
        self.reload_button = QPushButton('Reload')
        save_button.clicked.connect(self._save_settings)
        self.reload_button.clicked.connect(self._restart_app)

        button_layout.addWidget(save_button)
        button_layout.addWidget(self.reload_button)
        button_layout.addStretch()
        self.reload_button.hide()  # Hide reload button for now, as restart is required to apply changes

        layout.addLayout(button_layout)
        layout.addStretch()

    def _restart_app(self) -> None:
        """Restart the application using the current interpreter (WindowButtons pattern)."""
        import sys
        from pathlib import Path
        from PyQt6.QtCore import QProcess
        from PyQt6.QtWidgets import QApplication
        from core.errors import log, log_exception
        try:
            executable = sys.executable
            script_path = Path(sys.argv[0]).resolve()
            if script_path.suffix.lower() == '.py':
                program = executable
                args = [str(script_path), *sys.argv[1:]]
            else:
                program = executable
                args = list(sys.argv[1:])
            started = QProcess.startDetached(program, args)
            if not started:
                log('ERROR', 'Failed to start restart process',
                    category='settings', action='restart')
                return
            log('INFO', 'Restarting application from settings',
                category='settings', action='restart')
            QApplication.instance().quit()
        except Exception as exc:
            log_exception(exc, 'Failed to restart application',
                          category='settings', action='restart')

    def _add_input(
        self,
        layout: QFormLayout,
        label_text: str,
        key: str,
        placeholder: str,
        is_password: bool = False
    ) -> None:
        """Add a labeled line edit to the form layout."""
        label = QLabel(label_text)
        label.setFont(get_fonts(FONT.input_lbl))

        input_field = QLineEdit()
        input_field.setFont(get_fonts(FONT.input_field))
        input_field.setPlaceholderText(placeholder)
        if is_password:
            input_field.setEchoMode(QLineEdit.EchoMode.Password)

        layout.addRow(label, input_field)
        self.inputs[key] = input_field

    def _load_settings(self) -> None:
        """Load settings from disk and populate inputs."""
        try:
            settings = load_user_settings()
            mongo_settings = settings.get('mongodb', {}) if isinstance(settings, dict) else {}
            defaults = self._get_default_mongo_settings()

            for key, input_field in self.inputs.items():
                value = mongo_settings.get(key)
                if isinstance(value, str):
                    value = value.strip()
                if not value:
                    value = defaults.get(key, '')
                input_field.setText(value or '')

            if self.status_label:
                self.status_label.setText('')
        except Exception as e:
            log_exception(e, 'Failed to load settings into UI', category='settings', action='load_ui')
            if self.status_label:
                self.status_label.setText('Failed to load settings.')

    def _save_settings(self) -> None:
        """Persist settings to disk."""
        try:
            current_settings = load_user_settings()
            if not isinstance(current_settings, dict):
                current_settings = {}

            mongo_settings = {}
            for key, input_field in self.inputs.items():
                value = input_field.text().strip()
                mongo_settings[key] = value if value else None

            current_settings['mongodb'] = mongo_settings
            save_user_settings(current_settings)
            self.reload_button.show()  # Show reload button to indicate restart is needed

            if self.status_label:
                self.status_label.setText('Saved. Restart the app to apply changes.')
            log('INFO', 'Settings saved from UI', category='settings', action='save_ui')
        except Exception as e:
            log_exception(e, 'Failed to save settings from UI', category='settings', action='save_ui')
            if self.status_label:
                self.status_label.setText('Failed to save settings.')

    def _get_default_mongo_settings(self) -> dict:
        """Return default MongoDB settings from environment or defaults."""
        return {
            'uri': os.getenv('MONGODB_URI', ''),
            'host': os.getenv('MONGODB_HOST', 'localhost:27017'),
            'database': os.getenv('MONGODB_DATABASE', 'stintflow'),
            'username': os.getenv('MONGODB_USERNAME', ''),
            'password': os.getenv('MONGODB_PASSWORD', ''),
            'auth_source': os.getenv('MONGODB_AUTH_SOURCE', 'admin')
        }

    def alert_db_connection_failure(self) -> None:
        """Display a message indicating the database connection failed."""
        dialog = PopUp(
            title="Database Connection Failed",
            message="Unable to connect to MongoDB. Please check your settings.",
            buttons=["Ok"],
            type="critical",
            parent=self
        )
        dialog.exec()
