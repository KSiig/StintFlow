from __future__ import annotations

from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout

from ui.components.common import ConfigButton, SectionHeader
from ....config import ConfigLayout


def _setup_ui(self) -> None:
    """Build header and container for agent cards."""
    layout = QVBoxLayout(self)
    layout.setContentsMargins(8, 8, 8, 8)
    layout.setSpacing(8)

    header_layout = QHBoxLayout()
    header_layout.setContentsMargins(0, 0, 0, 0)
    header_layout.setSpacing(4)

    header = SectionHeader(
        title="Agent Overview",
        icon_path="resources/icons/race_config/radio.svg",
        icon_color="#05fd7e",
        icon_size=ConfigLayout.ICON_SIZE,
        spacing=ConfigLayout.HEADER_SPACING,
    )
    header_layout.addWidget(header)
    header_layout.addStretch()

    btn = ConfigButton(
        "",
        icon_path="resources/icons/race_config/cloud-sync.svg",
        width_type="min",
        icon_size=12,
    )
    btn.clicked.connect(self._load_agents)
    header_layout.addWidget(btn)

    layout.addLayout(header_layout)

    self._cards_layout = QVBoxLayout()
    layout.addLayout(self._cards_layout)
