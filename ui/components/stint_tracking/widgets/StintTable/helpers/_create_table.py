from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QAbstractItemView, QHeaderView, QTableView, QSizePolicy

from ui.utilities import FONT, get_fonts
from ....delegates import BackgroundRespectingDelegate
from ....table import SpacedHeaderView
from ....constants import VERTICAL_HEADER_WIDTH


def _create_table(self, focus: bool):
    """Create and configure the QTableView instance."""
    table = QTableView(self)
    table.setShowGrid(False)
    table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
    table.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
    table.setObjectName("StintsTable")
    table.setItemDelegate(BackgroundRespectingDelegate(table))

    custom_header = SpacedHeaderView(Qt.Orientation.Horizontal, table)
    table.setHorizontalHeader(custom_header)

    if not focus:
        table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        table.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    self._setup_vertical_header(table)
    self._setup_horizontal_header(table)

    vh = table.verticalHeader()
    vh.setStyleSheet(
        f"QHeaderView::section {{ "
        f"font-family: {self.font_table_cell.family()}; "
        f"font-size: {self.font_table_cell.pointSize()}pt; "
        f"padding-left: {self.VERTICAL_HEADER_PADDING_LEFT}px; "
        f"}}"
    )
    vh.setFixedWidth(VERTICAL_HEADER_WIDTH)
    return table
