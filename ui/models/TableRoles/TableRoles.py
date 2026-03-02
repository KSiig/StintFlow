"""Custom Qt item data roles for the stint table."""

from PyQt6.QtCore import Qt


class TableRoles:
    """Custom Qt item data roles for stint table."""

    TiresRole = Qt.ItemDataRole.UserRole + 1
    MetaRole = Qt.ItemDataRole.UserRole + 2
