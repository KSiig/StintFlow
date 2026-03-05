from __future__ import annotations

from core.errors import log_exception

from ._sort_agents_by_status import _sort_agents_by_status


def _load_agents(self) -> None:
    """Query database for agents and refresh the overview."""
    try:
        from core.database.connection import get_agents_collection

        agents_col = get_agents_collection()
        selection_model = getattr(self, 'selection_model', None)
        session_id = getattr(selection_model, 'session_id', None)

        if session_id is None:
            agents = []
        else:
            agents = list(agents_col.find({'session_id': str(session_id)}))
            agents = _sort_agents_by_status(agents)

        if agents:
            self._empty_agent_reads = 0
            self._last_agents = agents
            self._update_summary_label(agents)
            self._popup.set_agents(agents)
            return

        self._empty_agent_reads = getattr(self, '_empty_agent_reads', 0) + 1

        if self._empty_agent_reads < 3 and self._last_agents:
            self._update_summary_label(self._last_agents)
            self._popup.set_agents(self._last_agents)
            return

        self._last_agents = []
        self._update_summary_label([])
        self._popup.set_agents([])
    except Exception as e:
        log_exception(
            e,
            'Failed to load agents',
            category='agent_overview',
            action='load_agents',
        )
