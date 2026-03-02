from __future__ import annotations

from PyQt6.QtWidgets import QHBoxLayout, QSizePolicy

from ui.models import ModelContainer
from ...StrategySettings import StrategySettings
from ....widgets import StintTable


def _setup_ui(self) -> None:
    """Set up the strategy tab UI layout."""
    layout = QHBoxLayout(self)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(12)

    models = ModelContainer(
        selection_model=self.selection_model,
        table_model=self.table_model,
    )

    strategy_settings = StrategySettings(self, models, self.strategy)
    self.strategy_settings = strategy_settings
    strategy_settings.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    strategy_settings.setFixedWidth(256)
    strategy_settings.strategy_updated.connect(self._strategy_updated)
    strategy_settings.strategy_deleted.connect(self._on_settings_deleted)
    layout.addWidget(strategy_settings, stretch=1)

    self.stint_table = StintTable(
        models=models,
        focus=True,
        auto_update=False,
        allow_editors=False,
    )
    layout.addWidget(self.stint_table, stretch=1)

    self.setLayout(layout)
