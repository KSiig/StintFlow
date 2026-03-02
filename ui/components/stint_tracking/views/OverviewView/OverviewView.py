"""Overview view for stint tracking."""

from PyQt6.QtWidgets import QWidget

from ui.models import ModelContainer

from .helpers import _build_layout


class OverviewView(QWidget):
    """View for stint tracking overview."""

    _build_layout = _build_layout

    def __init__(self, models: ModelContainer) -> None:
        super().__init__()
        self.selection_model = models.selection_model
        self.table_model = models.table_model
        self._build_layout(models)
