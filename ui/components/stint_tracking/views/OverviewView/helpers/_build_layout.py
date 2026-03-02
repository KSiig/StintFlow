"""Build the OverviewView layout."""

from PyQt6.QtWidgets import QVBoxLayout

from ui.components.stint_tracking.widgets import StintTable


def _build_layout(self, models) -> None:
    """Compose the stint table with editing enabled."""
    layout = QVBoxLayout(self)

    stint_table = StintTable(
        models=models,
        focus=True,
        auto_update=True,
        allow_editors=True,
        enable_actions=True,
    )

    layout.addWidget(stint_table)
