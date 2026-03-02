"""Create a title label for configuration fields."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QSizePolicy

from ui.utilities import FONT, get_fonts


def create_config_label(title: str) -> QLabel:
    """Return a QLabel configured for config field titles."""
    title_label = QLabel(title)
    title_label.setObjectName("SettingTitle")
    title_label.setFont(get_fonts(FONT.input_lbl))
    title_label.setContentsMargins(0, 0, 0, 0)
    title_label.setSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
    title_label.setAlignment(Qt.AlignmentFlag.AlignTop)

    font_metrics = title_label.fontMetrics()
    title_label.setMaximumHeight(font_metrics.height())

    return title_label
