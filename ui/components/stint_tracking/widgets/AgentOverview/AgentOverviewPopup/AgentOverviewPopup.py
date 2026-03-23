from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget

from .bounded_functions._setup_ui import _setup_ui
from .bounded_functions.set_agents import set_agents
from ui.utilities import FONT, get_fonts


class AgentOverviewPopup(QWidget):
    """Floating list of agents that aligns under the overview control."""
    _setup_ui = _setup_ui
    set_agents = set_agents

    def __init__(self, parent=None):
        super().__init__(parent, Qt.WindowType.Popup)
        self.font_header = get_fonts(FONT.text_body_bold)
        self._setup_ui()

