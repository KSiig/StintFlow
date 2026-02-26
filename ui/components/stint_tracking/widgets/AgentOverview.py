from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel

from ui.models import ModelContainer
from core.utilities import resource_path
from core.errors import log_exception
from ui.components.common import SectionHeader
from ..config import (
    ConfigLayout, ConfigLabels,
)

class AgentOverview(QFrame):
    """Placeholder component shown below the main config options.

    Intended to be styled separately via its own stylesheet.  For now it just
    displays a label; future enhancements can add whatever additional settings
    or controls are required.
    """

    def __init__(self, models: ModelContainer = None) -> None:
        super().__init__()
        self.models = models
        self.setObjectName('AgentOverview')

        self._setup_styles()
        self._setup_ui()

    def _setup_styles(self) -> None:
        """Load and apply stylesheet specific to this component."""
        try:
            with open(resource_path('resources/styles/agent_overview.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError as e:
            log_exception(e, 'AgentOverview stylesheet not found',
                         category='agent_overview', action='load_stylesheet')

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(4)

        header = SectionHeader(
            title="Agent Overview",
            icon_path="resources/icons/race_config/radio.svg",
            icon_color="#05fd7e",
            icon_size=ConfigLayout.ICON_SIZE,
            spacing=ConfigLayout.HEADER_SPACING
        )
        layout.addWidget(header)

        self._show_agents() 

    def _show_agents(self):
        """Example method to demonstrate how this component could interact with the database."""
        try:
            from core.database.connection import get_agents_collection
            agents_col = get_agents_collection()
            agents = list(agents_col.find())
        except Exception as e:
            log_exception(e, 'Failed to fetch agents from database',
                         category='agent_overview', action='fetch_agents')