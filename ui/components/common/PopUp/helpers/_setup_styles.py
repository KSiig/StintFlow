"""Load and apply popup stylesheet."""

from core.errors import log
from core.utilities import resource_path


def _setup_styles(self) -> None:
    """Load QSS for the popup; warn if missing and continue."""
    try:
        with open(resource_path('resources/styles/popup.qss'), 'r') as f:
            self.setStyleSheet(f.read())
    except FileNotFoundError:
        log('WARNING', 'Popup stylesheet not found', category='popup', action='load_stylesheet')
