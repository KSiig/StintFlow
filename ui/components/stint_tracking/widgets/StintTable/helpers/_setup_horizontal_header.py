from __future__ import annotations

from ui.utilities import FONT, get_fonts


def _setup_horizontal_header(self, table) -> None:
    """Configure horizontal header font."""
    hh = table.horizontalHeader()
    font_table_header = self.font_table_header
    hh.setFont(font_table_header)
