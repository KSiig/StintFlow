"""Delegate for editing tire changes in the stint table."""

from PyQt6.QtWidgets import QStyledItemDelegate

from .helpers import (
    _find_view,
    _update_button_text,
    create_editor,
    help_event,
    paint,
    set_editor_data,
    set_model_data,
    update_editor_geometry,
)


class TireComboDelegate(QStyledItemDelegate):
    """Popup-based tire change selector with optional DB updates."""

    createEditor = create_editor
    setEditorData = set_editor_data
    setModelData = set_model_data
    updateEditorGeometry = update_editor_geometry
    paint = paint
    helpEvent = help_event
    _update_button_text = _update_button_text
    _find_view = _find_view

    def __init__(self, parent=None, update_doc: bool = False, strategy_id: str | None = None) -> None:
        super().__init__(parent)
        self.update_doc = update_doc
        self.strategy_id = strategy_id
        self.tires_changed = "0"
        self.lock_completed = False
        self.setObjectName("TireComboDelegate")
