"""Delegate that respects model BackgroundRole.

This module provides `BackgroundRespectingDelegate`, a minimal
`QStyledItemDelegate` subclass which paints a model-provided
`BackgroundRole` brush before rendering the standard item content.

Usage:
    delegate = BackgroundRespectingDelegate(parent)
    table.setItemDelegate(delegate)

This is useful when the model supplies per-row or per-cell background
colors (via `Qt.ItemDataRole.BackgroundRole`) but QSS or other delegates
would otherwise prevent that brush from being visible.
"""

from PyQt6.QtWidgets import QStyledItemDelegate
from PyQt6.QtCore import Qt


class BackgroundRespectingDelegate(QStyledItemDelegate):
    """QStyledItemDelegate that first fills the cell with the model's
    `BackgroundRole` brush (if present), then performs the normal paint
    operation.

    This ensures model-provided background tints are visible even when
    QSS or other delegate painting would otherwise obscure them.
    """

    def paint(self, painter, option, index):
        bg = index.data(Qt.ItemDataRole.BackgroundRole)
        if bg:
            painter.save()
            painter.fillRect(option.rect, bg)
            painter.restore()
        super().paint(painter, option, index)