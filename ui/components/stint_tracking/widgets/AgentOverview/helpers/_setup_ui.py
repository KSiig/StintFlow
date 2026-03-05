from __future__ import annotations

from PyQt6.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout

from ui.components.common.ConfigButton import ConfigButton
from ui.components.common.SectionHeader.SectionHeader import SectionHeader
from ....config import ConfigLayout


def _setup_ui(self) -> None:
    """Build header and container for agent cards."""
    layout = QHBoxLayout(self)
    layout.setContentsMargins(8, 0, 8, 0)
    layout.setSpacing(8)

    self._summary_label = QLabel("0 / 0 agents")
    self._summary_label.setObjectName("AgentOverviewSummary")
    layout.addWidget(self._summary_label)
