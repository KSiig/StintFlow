from __future__ import annotations

from core.errors import log
from core.utilities import resource_path


def _setup_styles(self) -> None:
    """Load and apply the strategy tab stylesheet."""
    try:
        with open(resource_path('resources/styles/strategy_tab.qss'), 'r') as f:
            self.setStyleSheet(f.read())
    except FileNotFoundError:
        log(
            'WARNING',
            'Strategy tab stylesheet not found',
            category='strategy_tab',
            action='load_stylesheet',
        )
