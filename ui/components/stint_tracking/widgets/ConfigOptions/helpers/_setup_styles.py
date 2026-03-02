from __future__ import annotations

from core.errors import log_exception
from core.utilities import resource_path


def _setup_styles(self) -> None:
    """Load stylesheet for config options panel."""
    try:
        with open(resource_path('resources/styles/config_options.qss'), 'r') as f:
            self.setStyleSheet(f.read())
    except Exception as e:
        log_exception(
            e,
            'Failed to load config_options stylesheet',
            category='ui',
            action='load_stylesheet',
        )
