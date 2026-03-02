from __future__ import annotations

from core.errors import log
from core.utilities import resource_path


def _setup_styles(self) -> None:
    """Load and apply the strategy settings stylesheet."""
    try:
        with open(resource_path('resources/styles/strategy_settings.qss'), 'r') as f:
            self.setStyleSheet(f.read())
    except FileNotFoundError:
        log(
            'WARNING',
            'Strategy settings stylesheet not found',
            category='strategy_settings',
            action='load_stylesheet',
        )
