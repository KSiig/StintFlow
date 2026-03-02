from PyQt6.QtWidgets import QVBoxLayout, QWidget, QScrollArea

from ..constants import WORKSPACE_MARGINS_BOT, WORKSPACE_MARGINS_HOR, WORKSPACE_MARGINS_VER


def create_right_pane(scroll_area: QScrollArea) -> QWidget:
    """Create the right pane containing the scrollable content area."""
    pane = QWidget()
    layout = QVBoxLayout(pane)
    layout.setContentsMargins(
        WORKSPACE_MARGINS_HOR,
        WORKSPACE_MARGINS_VER,
        WORKSPACE_MARGINS_HOR,
        WORKSPACE_MARGINS_BOT,
    )
    layout.setSpacing(0)
    layout.addWidget(scroll_area)
    return pane
