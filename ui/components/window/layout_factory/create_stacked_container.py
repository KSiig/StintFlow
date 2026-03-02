from PyQt6.QtWidgets import QStackedLayout, QWidget, QScrollArea


def create_stacked_container(scroll_area: QScrollArea) -> tuple[QWidget, QStackedLayout]:
    """Create a stacked container inside the provided scroll area."""
    container = QWidget()
    layout = QStackedLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    scroll_area.setWidget(container)
    return container, layout
