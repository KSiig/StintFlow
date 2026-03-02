from PyQt6.QtCore import Qt

from ui.components.stint_tracking import get_header_icon
from ui.utilities import FONT
from ui.utilities.load_icon import load_icon

from ..constants import HEADER_ICON_COLOR, VERTICAL_HEADER_START_INDEX


def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.ItemDataRole.DisplayRole):  # type: ignore[override]
    """Return header labels or icons for the table."""
    if orientation == Qt.Orientation.Horizontal and section < len(self.headers):
        if role == Qt.ItemDataRole.DisplayRole:
            return self.headers[section]
        if role == Qt.ItemDataRole.DecorationRole:
            icon_file = get_header_icon(section)
            icon_path = f"resources/icons/table_headers/{icon_file}"
            return load_icon(icon_path, color=HEADER_ICON_COLOR)
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

    elif orientation == Qt.Orientation.Vertical:
        if role == Qt.ItemDataRole.DisplayRole:
            return section + VERTICAL_HEADER_START_INDEX
        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter

    return None
