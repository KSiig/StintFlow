"""Load and apply dropdown stylesheet."""

from core.errors import log, log_exception
from core.utilities import resource_path


def _setup_styles(self) -> None:
    """Load QSS for the dropdown; warn but continue if missing."""
    try:
        with open(resource_path('resources/styles/dropdown.qss'), 'r') as f:
            self.setStyleSheet(f.read())
    except FileNotFoundError:
        log('WARNING', 'Dropdown stylesheet not found', category='dropdown', action='load_stylesheet')
    except Exception as exc:
        log_exception(exc, 'Error loading dropdown stylesheet', category='dropdown', action='load_stylesheet')
