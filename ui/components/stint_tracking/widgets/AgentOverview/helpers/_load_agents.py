from __future__ import annotations

from core.errors import log_exception


def _load_agents(self) -> None:
    """Query database for agents and refresh the overview."""
    try:
        from core.database.connection import get_agents_collection

        agents_col = get_agents_collection()
        agents = list(agents_col.find())
        self._last_agents = agents
        self._update_summary_label(agents)
        self._popup.set_agents(agents)
    except Exception as e:
        log_exception(
            e,
            'Failed to load agents',
            category='agent_overview',
            action='load_agents',
        )
