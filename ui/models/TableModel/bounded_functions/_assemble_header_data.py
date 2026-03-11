"""Utilities for TableModel header data (labels, icons, alignment)."""

from PyQt6.QtCore import Qt

from ui.components.stint_tracking import get_header_icon
from ui.utilities.load_icon import load_icon
from core.utilities import resource_path
import os

from ..constants import HEADER_ICON_COLOR, VERTICAL_HEADER_START_INDEX
from core.errors.log_error.log import log


def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):  # type: ignore[override]
    """Return header labels, icons, or alignment for the table.

    Parameters:
    section (int): The index of the header section.
    orientation (Qt.Orientation): The orientation of the header (horizontal or vertical).
    role (int): The Qt role for which data is requested (e.g., DisplayRole, DecorationRole, TextAlignmentRole).

    Returns:
    Any: The data for the requested role, which can be a string (label), QIcon (icon), or alignment flags.

    Behavior:
    - For DisplayRole:
      - Horizontal headers return the corresponding label from `self.headers`.
      - Vertical headers return the section index adjusted by `VERTICAL_HEADER_START_INDEX`.
    - For DecorationRole:
      - Horizontal headers return an icon loaded from the `resources/icons/table_headers/` directory.
    - For TextAlignmentRole:
      - Both horizontal and vertical headers return left-aligned and vertically centered alignment.

    Special Cases:
    - If the section index is out of range for horizontal headers, None is returned.
    - Assumes `self.headers` contains the header labels for horizontal orientation.
    """
    if orientation == Qt.Orientation.Horizontal and section < len(self.headers):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        if role == Qt.ItemDataRole.DecorationRole:
            icon_file = get_header_icon(section)
            rel_path = f"resources/icons/table_headers/{icon_file}"
            abs_path = resource_path(rel_path)
            if os.path.exists(abs_path):
                # load_icon will resolve via resource_path itself, so give it
                # the relative path to avoid double resolution
                return load_icon(rel_path, color=HEADER_ICON_COLOR)
            else:
                log(
                    "WARNING",
                    f"Icon file not found: {abs_path}",
                    category="ui",
                    action="load_icon",
                )
                return None
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

    elif orientation == Qt.Orientation.Vertical:
        if role == Qt.ItemDataRole.DisplayRole:
            return section + VERTICAL_HEADER_START_INDEX
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

    return None
