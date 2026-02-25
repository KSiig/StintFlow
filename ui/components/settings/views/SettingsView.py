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
from PyQt6.QtGui import QIntValidator

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
        """Build the settings UI layout.

        Frames are composed by helper methods so it's easier to add new
        sections (e.g. logging) without the method growing unwieldy.
        """
        frame = QFrame()
        frame.setObjectName('SettingsFrame')
        frame.setFixedWidth(512)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(frame)

        layout = QVBoxLayout(frame)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(16)

        # add each section via helper methods
        self._build_agent_section(layout)
        self._build_mongo_section(layout)
        self._build_logging_section(layout)
        self._build_status_section(layout)
        self._build_button_section(layout)
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

    # ------------------------------------------------------------------
    # section builders
    # ------------------------------------------------------------------
    def _build_agent_section(self, parent_layout: QVBoxLayout) -> None:
        """Create a settings frame that allows the user to specify a custom
        agent name for stint tracker processes.

        The value is optional; if the field is left blank the tracker will
        fall back to a PID‑based default.  Providing a name here can help when
        multiple trackers are run on the same machine (e.g. testing).
        """
        agent_frame = QFrame()
        agent_frame.setObjectName('AgentFrame')
        agent_layout = QVBoxLayout(agent_frame)
        agent_layout.setContentsMargins(0, 0, 0, 0)
        agent_layout.setSpacing(12)

        title = QLabel('Tracker agent')
        title.setFont(get_fonts(FONT.header_nav))
        agent_layout.addWidget(title)

        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(8)
        form_layout.setHorizontalSpacing(24)

        self._add_input(form_layout, 'Agent name', 'agent_name', 'stint_tracker_<pid>')

        agent_layout.addLayout(form_layout)
        parent_layout.addWidget(agent_frame)

    def _build_mongo_section(self, parent_layout: QVBoxLayout) -> None:
        """Construct the MongoDB settings frame and add it to the parent layout."""
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
        parent_layout.addWidget(mongo_frame)

    def _build_status_section(self, parent_layout: QVBoxLayout) -> None:
        """Create hint and status label widgets."""
        hint = QLabel('Connection string overrides host and credentials when set.')
        hint.setFont(get_fonts(FONT.header_input_hint))
        parent_layout.addWidget(hint)

        self.status_label = QLabel('')
        self.status_label.setFont(get_fonts(FONT.header_input_hint))
        parent_layout.addWidget(self.status_label)

    def _build_logging_section(self, parent_layout: QVBoxLayout) -> None:
        """Create the logging settings frame with a single numeric field."""
        log_frame = QFrame()
        log_frame.setObjectName('LogFrame')
        log_layout = QVBoxLayout(log_frame)
        log_layout.setContentsMargins(0, 0, 0, 0)
        log_layout.setSpacing(12)

        title = QLabel('Logging')
        title.setFont(get_fonts(FONT.header_nav))
        log_layout.addWidget(title)

        form_layout = QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(8)
        form_layout.setHorizontalSpacing(24)

        # retention days field (integer only)
        label = QLabel('Log retention (days)')
        label.setFont(get_fonts(FONT.input_lbl))
        retention_input = QLineEdit()
        retention_input.setFont(get_fonts(FONT.input_field))
        retention_input.setPlaceholderText('7')
        retention_input.setValidator(QIntValidator(0, 3650, self))
        form_layout.addRow(label, retention_input)
        self.inputs['retention_days'] = retention_input

        log_layout.addLayout(form_layout)
        parent_layout.addWidget(log_frame)

    def _build_button_section(self, parent_layout: QVBoxLayout) -> None:
        """Construct the save/reload button row."""
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

        parent_layout.addLayout(button_layout)

    def _load_settings(self) -> None:
        """Load settings from disk and populate inputs."""
        try:
            settings = load_user_settings()
            mongo_settings = settings.get('mongodb', {}) if isinstance(settings, dict) else {}
            logging_settings = settings.get('logging', {}) if isinstance(settings, dict) else {}
            agent_settings = settings.get('agent', {}) if isinstance(settings, dict) else {}
            mongo_defaults = self._get_default_mongo_settings()
            log_defaults = self._get_default_logging_settings()
            agent_defaults = self._get_default_agent_settings()

            # populate agent field
            agent_field = self.inputs.get('agent_name')
            if agent_field is not None:
                value = agent_settings.get('name')
                if isinstance(value, str):
                    value = value.strip()
                if not value:
                    value = agent_defaults.get('name', '')
                agent_field.setText(value or '')

            # populate mongo fields
            for key in ('uri', 'host', 'database', 'username', 'password', 'auth_source'):
                input_field = self.inputs.get(key)
                if not input_field:
                    continue
                value = mongo_settings.get(key)
                if isinstance(value, str):
                    value = value.strip()
                if not value:
                    value = mongo_defaults.get(key, '')
                input_field.setText(value or '')

            # populate logging field
            retention_field = self.inputs.get('retention_days')
            if retention_field is not None:
                value = logging_settings.get('retention_days')
                if value is None:
                    value = log_defaults.get('retention_days', '')
                retention_field.setText(str(value) if value is not None else '')

            if self.status_label:
                self.status_label.setText('')
        except Exception as e:
            log_exception(e, 'Failed to load settings into UI', category='settings', action='load_ui')
            if self.status_label:
                self.status_label.setText('Failed to load settings.')

    def _get_default_agent_settings(self) -> dict:
        """Return default agent-related settings.

        The only supported key at the moment is ``name``.  By default we allow
        an environment variable so the program can be configured externally
        (useful for testing or CI where the UI may not be used).
        """
        return {
            'name': os.getenv('AGENT_NAME', '')
        }

    def _get_default_logging_settings(self) -> dict:
        """Return default logging settings from environment or sane defaults."""
        return {
            'retention_days': int(os.getenv('LOG_RETENTION_DAYS', '7'))
        }

    def _save_settings(self) -> None:
        """Persist settings to disk."""
        try:
            current_settings = load_user_settings()
            if not isinstance(current_settings, dict):
                current_settings = {}

            mongo_settings = {}
            # known mongo keys ensure we don't accidentally include logging
            # agent settings
            agent_settings = {}
            agent_field = self.inputs.get('agent_name')
            if agent_field is not None:
                text = agent_field.text().strip()
                agent_settings['name'] = text if text else None

            for key in ('uri', 'host', 'database', 'username', 'password', 'auth_source'):
                input_field = self.inputs.get(key)
                if input_field is None:
                    continue
                value = input_field.text().strip()
                mongo_settings[key] = value if value else None

            logging_settings = {}
            retention_field = self.inputs.get('retention_days')
            if retention_field is not None:
                text = retention_field.text().strip()
                logging_settings['retention_days'] = int(text) if text else None

            current_settings['agent'] = agent_settings

            current_settings['mongodb'] = mongo_settings
            current_settings['logging'] = logging_settings
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
