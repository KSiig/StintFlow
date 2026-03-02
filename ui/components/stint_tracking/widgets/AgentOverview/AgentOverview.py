"""Agent overview widget displaying connected agents."""

from PyQt6.QtWidgets import QFrame

from ui.utilities.load_style import load_style
from .AgentCard import AgentCard
from .helpers import _load_agents, _setup_ui, set_agents


class AgentOverview(QFrame):
    """Render agent cards with last heartbeat indicators."""

    _setup_ui = _setup_ui
    _load_agents = _load_agents
    set_agents = set_agents

    AgentCard = AgentCard

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName('AgentOverview')

        self._cards_layout = None

        load_style('resources/styles/stint_tracking/agent_overview.qss', widget=self)
        self._setup_ui()
