from __future__ import annotations

from PyQt6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QFrame

from ui.components.common.ConfigButton import ConfigButton
from ui.components.common.SectionHeader.SectionHeader import SectionHeader
from ....config import ConfigLayout


def _setup_ui(self: QFrame) -> None:
    """Build header and container for agent cards."""
    layout = QHBoxLayout(self)
    layout.setContentsMargins(8, 0, 8, 0)
    layout.setSpacing(8)

    self._summary_label = QLabel("0 / 0 agents")
    self._summary_label.setObjectName("AgentOverviewSummary")
    self._summary_label.setFont(self.font_summary)
    layout.addWidget(self._summary_label)
