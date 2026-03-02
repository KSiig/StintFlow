from PyQt6.QtCore import Qt


def _get_editable_flags(self):
    """Return standard flags for editable cells."""
    return (
        Qt.ItemFlag.ItemIsSelectable
        | Qt.ItemFlag.ItemIsEnabled
        | Qt.ItemFlag.ItemIsEditable
    )
