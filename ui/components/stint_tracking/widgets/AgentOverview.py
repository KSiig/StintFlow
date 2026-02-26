from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt

from datetime import datetime, timedelta

from core.utilities import resource_path
from core.errors import log_exception
from ui.components.common import SectionHeader, ConfigButton
from ..config import (
    ConfigLayout,
)
from ui.utilities import get_fonts, FONT


class AgentOverview(QFrame):
    """Widget that displays a list of connected agents as individual cards.

    The caller should invoke ``set_agents`` with a list of Mongo-style documents
    (each containing ``name``, ``connected_at`` and ``last_heartbeat``) and
    this widget will render a card for each one.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setObjectName('AgentOverview')

        self._setup_styles()
        self._setup_ui()

    def _setup_styles(self) -> None:
        try:
            with open(resource_path('resources/styles/agent_overview.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError as e:
            log_exception(e, 'AgentOverview stylesheet not found',
                         category='agent_overview', action='load_stylesheet')

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # header area with title on left and action button on right
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        header_layout.setSpacing(4)

        header = SectionHeader(
            title="Agent Overview",
            icon_path="resources/icons/race_config/radio.svg",
            icon_color="#05fd7e",
            icon_size=ConfigLayout.ICON_SIZE,
            spacing=ConfigLayout.HEADER_SPACING
        )
        header_layout.addWidget(header)
        header_layout.addStretch()

        # placeholder button; will be wired up later
        btn = ConfigButton("", icon_path="resources/icons/race_config/cloud-sync.svg", width_type="min", icon_size=12)
        btn.clicked.connect(self._load_agents)
        header_layout.addWidget(btn)

        layout.addLayout(header_layout)

        self._cards_layout: QVBoxLayout | None = QVBoxLayout()
        layout.addLayout(self._cards_layout)

    def set_agents(self, agents: list[dict]) -> None:
        """Render a card for each agent in ``agents``.

        Existing cards are removed before the new list is shown.
        """
        if self._cards_layout is None:
            return

        while self._cards_layout.count():
            item = self._cards_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        for agent in agents:
            self._cards_layout.addWidget(self.AgentCard(agent))

    def _load_agents(self) -> None:
        """Query the database for agents and update the overview."""
        try:
            from core.database.connection import get_agents_collection
            agents_col = get_agents_collection()
            agents = list(agents_col.find())
            self.set_agents(agents)
        except Exception as e:
            log_exception(e, 'Failed to load agents',
                         category='agent_overview', action='load_agents')

    class AgentCard(QFrame):
        """Individual frame showing a single agent's details."""

        def __init__(self, agent: dict) -> None:
            super().__init__()
            self.setObjectName('AgentCard')

            layout = QVBoxLayout(self)
            layout.setContentsMargins(6, 6, 6, 6)
            layout.setSpacing(2)

            def _format_ts(val):
                # Accept datetime objects or ISO strings; return formatted text
                if isinstance(val, datetime):
                    ts = val
                else:
                    try:
                        ts = datetime.fromisoformat(str(val))
                    except Exception:
                        return str(val)
                # if the timestamp is naive assume UTC (our DB writes UTC)
                if ts.tzinfo is None:
                    from datetime import timezone
                    ts = ts.replace(tzinfo=timezone.utc)
                # convert to local timezone before formatting
                try:
                    ts = ts.astimezone()
                except Exception:
                    pass
                age = datetime.now(ts.tzinfo) - ts
                if age > timedelta(days=1):
                    return ts.strftime("%d-%m/%y %H:%M")
                else:
                    return ts.strftime("%H:%M")

            for field in ['name', 'connected_at', 'last_heartbeat']:
                if field not in agent:
                    log_exception(
                        ValueError(f'Missing expected field "{field}" in agent document'),
                        f'Agent document missing "{field}"',
                        category='agent_overview', action='render_agent_card'
                    )
                raw = agent.get(field, 'N/A')
                value = raw
                if field in ('connected_at', 'last_heartbeat') and raw != 'N/A':
                    value = _format_ts(raw)
                lbl = QLabel(f"{field.capitalize()}: {value}")
                lbl.setFont(get_fonts(FONT.input_lbl))
                # tooltip shows unformatted value for time fields
                if field in ('connected_at', 'last_heartbeat') and raw != 'N/A':
                    lbl.setToolTip(str(raw))
                layout.addWidget(lbl)
