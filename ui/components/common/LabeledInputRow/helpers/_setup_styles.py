"""Helper to load styles for the labeled input row."""

from core.errors import log
from core.utilities import resource_path


def _setup_styles(self) -> None:
    """Load and apply the stylesheet; degrade gracefully if missing."""
    try:
        with open(resource_path('resources/styles/labeled_input_row.qss'), 'r') as f:
            self.setStyleSheet(f.read())
    except FileNotFoundError:
        log('WARNING', 'Labeled input row stylesheet not found',
            category='labeled_input_row', action='load_stylesheet')
