"""Build the strategy settings section."""

from PyQt6.QtGui import QIntValidator
from PyQt6.QtWidgets import QFormLayout, QFrame, QLabel, QLineEdit, QVBoxLayout

from ui.utilities import FONT, get_fonts


def _build_strategy_section(self, parent_layout: QVBoxLayout) -> None:
    """Create UI controls for strategy-related settings."""
    strat_frame = QFrame()
    strat_frame.setObjectName("StrategyFrame")
    strat_layout = QVBoxLayout(strat_frame)
    strat_layout.setContentsMargins(0, 0, 0, 0)
    strat_layout.setSpacing(12)

    title = QLabel("Strategy")
    title.setFont(get_fonts(FONT.header_nav))
    strat_layout.addWidget(title)

    form_layout = QFormLayout()
    form_layout.setContentsMargins(0, 0, 0, 0)
    form_layout.setSpacing(8)
    form_layout.setHorizontalSpacing(24)

    # auto-sync interval
    label = QLabel("Auto-sync interval (sec)")
    label.setFont(get_fonts(FONT.input_lbl))
    interval_input = QLineEdit()
    interval_input.setFont(get_fonts(FONT.input_field))
    interval_input.setPlaceholderText("5")
    interval_input.setValidator(QIntValidator(1, 86400, self))
    form_layout.addRow(label, interval_input)
    self.inputs["strategy_auto_sync_interval_seconds"] = interval_input

    strat_layout.addLayout(form_layout)
    parent_layout.addWidget(strat_frame)
