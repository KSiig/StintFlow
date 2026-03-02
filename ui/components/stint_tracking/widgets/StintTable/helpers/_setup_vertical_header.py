from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetrics
from PyQt6.QtWidgets import QAbstractButton, QHBoxLayout, QLabel, QTableView, QWidget

from ui.utilities import FONT, get_fonts, load_icon
from ....constants import VERTICAL_HEADER_LABEL, VERTICAL_HEADER_WIDTH


def _setup_vertical_header(self, table: QTableView) -> None:
    """Configure vertical header appearance and corner widget."""
    vh = table.verticalHeader()

    font_table_cell = get_fonts(FONT.table_cell)
    font_table_header = get_fonts(FONT.table_header)

    vh.setDefaultAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

    font_metrics = QFontMetrics(font_table_cell)
    row_height = font_metrics.height() + self.ROW_PADDING_VERTICAL
    vh.setDefaultSectionSize(row_height)

    self._setup_corner_button(table, vh, font_table_header)
