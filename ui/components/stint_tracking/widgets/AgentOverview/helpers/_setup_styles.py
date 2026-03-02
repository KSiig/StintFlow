from __future__ import annotations

from core.errors import log_exception
from core.utilities import resource_path


def _setup_styles(self) -> None:
    """Load QSS for agent overview cards."""
    try:
        with open(resource_path('resources/styles/agent_overview.qss'), 'r') as f:
            self.setStyleSheet(f.read())
    except FileNotFoundError as e:
        log_exception(
            e,
            'AgentOverview stylesheet not found',
            category='agent_overview',
            action='load_stylesheet',
        )
