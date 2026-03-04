"""Agent overview widget displaying connected agents."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame

from ui.utilities.load_style import load_style
from .AgentCard import AgentCard
from .AgentOverviewPopup import AgentOverviewPopup
from .helpers import (
    _handle_mouse_release,
    _load_agents,
    _open_popup,
    _setup_ui,
    _update_summary_label,
)


class AgentOverview(QFrame):
    """Render agent cards with last heartbeat indicators."""

    _setup_ui = _setup_ui
    _load_agents = _load_agents
    _update_summary_label = _update_summary_label
    _open_popup = _open_popup

    mouseReleaseEvent = _handle_mouse_release

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName('AgentOverview')

        self._last_agents: list[dict] = []
        self._empty_agent_reads = 0
        self._popup = AgentOverviewPopup(self)

        load_style('resources/styles/stint_tracking/agent_overview/agent_overview.qss', widget=self)
        self._setup_ui()
