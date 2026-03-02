"""Load and apply navigation menu stylesheet."""

from core.errors import log_exception
from core.utilities import resource_path


def _setup_styles(self) -> None:
    """Load navigation menu stylesheet and log if missing."""
    try:
        with open(resource_path('resources/styles/navigation_menu.qss'), 'r') as f:
            self.setStyleSheet(f.read())
    except FileNotFoundError as exc:
        log_exception(exc, 'Navigation menu stylesheet not found', category='ui', action='load_stylesheet')
