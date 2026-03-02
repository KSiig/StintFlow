"""Delegate providing action buttons for completed stints."""

from PyQt6.QtCore import Qt, QRect, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QStyledItemDelegate

from ui.models.TableRoles import TableRoles
from ui.models.table_constants import ColumnIndex

from .helpers import (
    _button_rects,
    _draw_button,
    _emit_button_signals,
    _handle_mouse_click,
    _persist_excluded_flag,
    _toggle_exclude,
    editor_event,
    help_event,
    paint,
)


class ActionsDelegate(QStyledItemDelegate):
    """Render exclude/delete action buttons in the actions column."""

    excludeClicked = pyqtSignal(int)
    deleteClicked = pyqtSignal(int, str)
    buttonClicked = pyqtSignal(str, int)

    _draw_button = _draw_button
    _button_rects = _button_rects
    _handle_mouse_click = _handle_mouse_click
    _toggle_exclude = _toggle_exclude
    _persist_excluded_flag = _persist_excluded_flag
    _emit_button_signals = _emit_button_signals
    helpEvent = help_event
    paint = paint
    editorEvent = editor_event

    def __init__(self, parent=None, background_color: str = "#0e4c35", text_color: str = "#B0B0B0", update_doc: bool = False, strategy_id: str | None = None):
        super().__init__(parent)
        self.background_color = QColor(background_color)
        self.text_color = QColor(text_color)
        self.border_radius = 4
        self.button_width = 20
        self.spacing = 4
        self.buttons = [
            {"name": "exclude", "icon": "resources/icons/table_cells/circle.svg"},
            {"name": "delete", "icon": "resources/icons/table_cells/trash.svg"},
        ]
        self.update_doc = update_doc
        self.strategy_id = strategy_id
