from __future__ import annotations

from PyQt6.QtWidgets import QFrame

from .bounded_functions import _paint_event, _set_status_color, _setup_ui
from ui.utilities.load_style import load_style
from ui.utilities import FONT, get_fonts


class AgentCard(QFrame):
    """Card showing a single agent's details."""

    _setup_ui = _setup_ui
    _set_status_color = _set_status_color
    # paintEvent = _paint_event

    def __init__(self, agent: dict) -> None:
        super().__init__()
        load_style('resources/styles/stint_tracking/agent_overview/agent_card.qss', widget=self)
        self.font_name = get_fonts(FONT.text_label_bold)
        self.font_status = get_fonts(FONT.text_caption)
        self.font_timestamps = get_fonts(FONT.text_label)

        self.setObjectName('AgentCard')
        self.heartbeat_dt = None
        self._setup_ui(agent)
