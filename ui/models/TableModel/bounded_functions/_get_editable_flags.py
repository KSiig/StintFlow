"""Provide standard editable flags for TableModel cells."""

from PyQt6.QtCore import Qt


def _get_editable_flags(self) -> Qt.ItemFlags:
    """Return standard flags for editable cells."""
    return (
        Qt.ItemFlag.ItemIsSelectable
        | Qt.ItemFlag.ItemIsEnabled
        | Qt.ItemFlag.ItemIsEditable
    )
