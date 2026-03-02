from __future__ import annotations

from PyQt6.QtWidgets import QHeaderView

from ....constants import COLUMN_WIDTHS, VERTICAL_HEADER_WIDTH


def _set_column_widths(self) -> None:
    """Apply fixed column widths and minimum table width."""
    hh = self.table.horizontalHeader()

    for col, width in COLUMN_WIDTHS.items():
        hh.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(col, width)

    header_length = hh.length() or 816
    min_width = header_length + VERTICAL_HEADER_WIDTH + self.MIN_WIDTH_EXTRA_PADDING
    self.table.setMinimumWidth(min_width)

    hh.setSectionsMovable(False)
    hh.setCascadingSectionResizes(False)
    hh.setHighlightSections(False)
