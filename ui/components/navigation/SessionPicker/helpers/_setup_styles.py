"""Load and apply session picker stylesheet."""

from PyQt6.QtWidgets import QSizePolicy
from core.errors import log_exception
from core.utilities import resource_path


def _setup_styles(self) -> None:
    """Load QSS and set basic object properties."""
    try:
        with open(resource_path('resources/styles/session_picker.qss'), 'r') as f:
            self.setStyleSheet(f.read())
    except FileNotFoundError as exc:
        log_exception(exc, 'Session picker stylesheet not found', category='ui', action='load_stylesheet')

    self.setObjectName("StintSelection")
    self.setSizePolicy(
        QSizePolicy.Policy.Minimum,
        QSizePolicy.Policy.Maximum,
    )
