from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QLabel,
    QScrollArea,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.utilities.load_style import load_style


def _setup_ui(self) -> None:
    """Create the floating widget layout for the agent overview."""
    self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
    self.setWindowFlag(Qt.WindowType.NoDropShadowWindowHint, True)
    self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)
    self.setObjectName("AgentOverviewPopup")

    load_style(
        "resources/styles/stint_tracking/agent_overview/agent_overview_popup.qss",
        widget=self,
    )

    container = QFrame(self)
    container.setObjectName("AgentOverviewPopupContainer")
    container.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)

    outer = QVBoxLayout(self)
    outer.setContentsMargins(0, 0, 0, 0)
    outer.setSpacing(0)
    outer.addWidget(container)

    layout = QVBoxLayout(container)
    layout.setContentsMargins(12, 12, 12, 12)
    layout.setSpacing(8)

    header = QLabel("Connected agents", container)
    header.setObjectName("AgentOverviewPopupHeader")
    layout.addWidget(header)

    scroll = QScrollArea(container)
    scroll.setObjectName("AgentOverviewPopupScroll")
    scroll.setFrameShape(QFrame.Shape.NoFrame)
    scroll.setWidgetResizable(True)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    scroll.setMinimumHeight(0)
    scroll.setMaximumHeight(420)

    content = QWidget()
    cards_layout = QVBoxLayout(content)
    cards_layout.setContentsMargins(0, 0, 0, 0)
    cards_layout.setSpacing(4)
    scroll.setWidget(content)

    layout.addWidget(scroll)

    self._cards_layout = cards_layout
    self._scroll_area = scroll
