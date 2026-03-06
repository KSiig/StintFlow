"""Build the StatsCard UI structure."""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QSizePolicy

from ui.utilities import FONT, get_fonts
from ui.utilities.load_icon import load_icon


def _setup_ui(self) -> None:
    """Create a vertical card with title/icon row and value row."""
    self.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

    layout = QVBoxLayout(self)
    layout.setContentsMargins(10, 8, 10, 8)
    layout.setSpacing(6)

    top_row = QHBoxLayout()
    top_row.setContentsMargins(0, 0, 0, 0)
    top_row.setSpacing(8)

    self.icon_label = QLabel(self)
    self.icon_label.setObjectName("StatsCardIcon")
    icon_pixmap = load_icon(self.icon_path, size=14, color=self.icon_color)
    if not icon_pixmap.isNull():
        self.icon_label.setPixmap(icon_pixmap)
        self.icon_label.setFixedSize(icon_pixmap.size())
    self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    top_row.addWidget(self.icon_label)

    self.title_label = QLabel(self.title, self)
    self.title_label.setObjectName("StatsCardTitle")
    self.title_label.setFont(get_fonts(FONT.text_caption))
    self.title_label.setAlignment(Qt.AlignmentFlag.AlignVCenter | Qt.AlignmentFlag.AlignLeft)
    self.title_label.setFont(self.font_title)
    top_row.addWidget(self.title_label)
    top_row.addStretch()

    self.value_label = QLabel(self.value_text, self)
    self.value_label.setObjectName("StatsCardValue")
    self.value_label.setFont(self.font_value)
    self.value_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

    value_row = QHBoxLayout()
    value_row.setContentsMargins(0, 0, 0, 0)
    value_row.setSpacing(4)
    value_row.addWidget(self.value_label)

    self.value_right_label = QLabel(self.value_right_text, self)
    self.value_right_label.setObjectName("StatsCardValueRight")
    self.value_right_label.setFont(self.font_title)
    self.value_right_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignBottom)
    self.value_right_label.setVisible(bool(self.value_right_text))
    value_row.addWidget(self.value_right_label)

    value_row.addStretch()

    layout.addLayout(top_row)
    layout.addLayout(value_row)
