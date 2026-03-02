"""Add a tab to the tab bar and stacked widget."""

from PyQt6.QtWidgets import QWidget


def _add_tab(self, widget: QWidget, label: str) -> None:
    """Add a tab with the given content widget and label."""
    self.tab_bar.addTab(label)
    self.stacked_widget.addWidget(widget)
