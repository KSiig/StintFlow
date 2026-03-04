from __future__ import annotations

from PyQt6.QtWidgets import QHeaderView

from ....constants import COLUMN_WIDTHS


def _set_column_widths(self) -> None:
    """Apply fixed column widths and minimum table width."""
    hh = self.table.horizontalHeader()

    for col, width in COLUMN_WIDTHS.items():
        hh.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
        self.table.setColumnWidth(col, width)

    hh.setSectionsMovable(False)
    hh.setCascadingSectionResizes(False)
    hh.setHighlightSections(False)
