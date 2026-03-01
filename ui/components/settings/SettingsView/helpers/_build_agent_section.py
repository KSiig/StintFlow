"""Build the tracker agent settings section."""

from PyQt6.QtWidgets import QFormLayout, QFrame, QLabel, QVBoxLayout

from ui.utilities import FONT, get_fonts


def _build_agent_section(self, parent_layout: QVBoxLayout) -> None:
    """Create settings for tracker agent name."""
    agent_frame = QFrame()
    agent_frame.setObjectName("AgentFrame")
    agent_layout = QVBoxLayout(agent_frame)
    agent_layout.setContentsMargins(0, 0, 0, 0)
    agent_layout.setSpacing(12)

    title = QLabel("Tracker agent")
    title.setFont(get_fonts(FONT.header_nav))
    agent_layout.addWidget(title)

    form_layout = QFormLayout()
    form_layout.setContentsMargins(0, 0, 0, 0)
    form_layout.setSpacing(8)
    form_layout.setHorizontalSpacing(24)

    self._add_input(form_layout, "Agent name", "agent_name", "stint_tracker_<pid>")

    agent_layout.addLayout(form_layout)
    parent_layout.addWidget(agent_frame)
