"""Settings view for application configuration."""

from PyQt6.QtWidgets import QLabel, QLineEdit, QPushButton, QWidget

from ui.models import ModelContainer

from .bounded_functions import alert_db_connection_failure
from .helpers import (
    _add_input,
    _build_agent_section,
    _build_button_section,
    _build_logging_section,
    _build_mongo_section,
    _build_status_section,
    _get_default_agent_settings,
    _get_default_logging_settings,
    _get_default_mongo_settings,
    _load_settings,
    _restart_app,
    _save_settings,
    _setup_styles,
    _setup_ui,
)


class SettingsView(QWidget):
    """Application settings view."""

    _setup_styles = _setup_styles
    _setup_ui = _setup_ui
    _add_input = _add_input
    _build_agent_section = _build_agent_section
    _build_mongo_section = _build_mongo_section
    _build_logging_section = _build_logging_section
    _build_status_section = _build_status_section
    _build_button_section = _build_button_section
    _load_settings = _load_settings
    _get_default_agent_settings = _get_default_agent_settings
    _get_default_logging_settings = _get_default_logging_settings
    _get_default_mongo_settings = _get_default_mongo_settings
    _save_settings = _save_settings
    _restart_app = _restart_app
    alert_db_connection_failure = alert_db_connection_failure

    def __init__(self, models: ModelContainer = None) -> None:
        super().__init__()
        self.models = models
        self.inputs: dict[str, QLineEdit] = {}
        self.status_label: QLabel | None = None
        self.reload_button: QPushButton | None = None

        self._setup_styles()
        self._setup_ui()
        self._load_settings()
