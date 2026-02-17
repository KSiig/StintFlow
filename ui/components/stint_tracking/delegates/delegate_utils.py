"""
Utility helpers for delegates in the stint tracking table.

Provides a small shared function to paint a model-provided
BackgroundRole so delegates don't duplicate the same code.
"""
from PyQt6.QtCore import Qt


def paint_model_background(painter, option, index):
    """Paint the model-provided BackgroundRole for this cell.

    Args:
        painter: QPainter instance
        option: QStyleOptionViewItem
        index: QModelIndex
    """
    bg = index.data(Qt.ItemDataRole.BackgroundRole)
    if bg:
        painter.save()
        painter.fillRect(option.rect, bg)
        painter.restore()
