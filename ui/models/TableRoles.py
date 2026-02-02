"""
Custom Qt item data roles for TableModel.

Extends Qt's standard roles with custom roles for tire data and metadata.
"""

from PyQt6.QtCore import Qt


class TableRoles:
    """
    Custom Qt item data roles for stint table.
    
    These roles allow storing and retrieving additional data beyond
    the standard DisplayRole, EditRole, etc.
    """
    
    # Custom role for tire data (compound, wear, flats, etc.)
    TiresRole = Qt.ItemDataRole.UserRole + 1
    
    # Custom role for metadata (document IDs, etc.)
    MetaRole = Qt.ItemDataRole.UserRole + 2
