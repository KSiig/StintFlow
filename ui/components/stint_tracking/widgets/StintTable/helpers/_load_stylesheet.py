from __future__ import annotations

from core.errors import log
from core.utilities import resource_path


def _load_stylesheet(self) -> None:
    """Load QSS stylesheet for stint table."""
    try:
        stylesheet_path = resource_path('resources/styles/stint_tracking/stint_table.qss')
        with open(stylesheet_path, 'r') as f:
            self.setStyleSheet(f.read())
    except FileNotFoundError:
        log('WARNING', f'Stylesheet not found: {resource_path("resources/styles/stint_tracking/stint_table.qss")}', category='stint_table', action='load_stylesheet')
    except Exception as e:
        log('ERROR', f'Failed to load stylesheet: {e}', category='stint_table', action='load_stylesheet')
