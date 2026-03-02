"""Delegate that respects model BackgroundRole."""

from PyQt6.QtWidgets import QStyledItemDelegate

from .helpers import _paint


class BackgroundRespectingDelegate(QStyledItemDelegate):
    """Paint model-provided BackgroundRole before default rendering."""

    paint = _paint
