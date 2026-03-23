from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractButton, QHBoxLayout, QLabel, QTableView, QWidget

from ui.utilities.load_icon import load_icon
from ....constants import VERTICAL_HEADER_LABEL, VERTICAL_HEADER_WIDTH


def _setup_corner_button(self, table: QTableView, vh, font_table_header) -> None:
    """Replace the default corner with custom label + icon."""
    corner = table.findChild(QAbstractButton)
    if not corner:
        return

    corner.hide()

    corner_replacement = QWidget(table)
    corner_replacement.setObjectName("StintTableCornerReplacement")
    corner_height = vh.defaultSectionSize() - self.CORNER_HEIGHT_ADJUSTMENT
    corner_replacement.setFixedSize(VERTICAL_HEADER_WIDTH, corner_height)
    corner_replacement.setStyleSheet("QWidget { background-color: #0c1327; border: none; }")

    corner_layout = QHBoxLayout(corner_replacement)
    corner_layout.setContentsMargins(self.CORNER_PADDING_LEFT, 0, self.CORNER_PADDING_RIGHT, 0)
    corner_layout.setSpacing(self.CORNER_ICON_SPACING)
    corner_layout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

    icon_label = QLabel()
    icon_path = "resources/icons/table_headers/hash.svg"
    icon_pixmap = load_icon(icon_path, color='#FFFFFF')
    icon_label.setPixmap(icon_pixmap)
    icon_label.setStyleSheet("background-color: transparent;")
    icon_label.setFixedSize(self.CORNER_ICON_SIZE, self.CORNER_ICON_SIZE)
    corner_layout.addWidget(icon_label)

    text_label = QLabel(VERTICAL_HEADER_LABEL)
    text_label.setFont(font_table_header)
    text_label.setStyleSheet("background-color: transparent; color: #ffffff;")
    corner_layout.addWidget(text_label)

    corner_layout.addStretch()

    corner_replacement.move(0, 0)
    corner_replacement.show()
