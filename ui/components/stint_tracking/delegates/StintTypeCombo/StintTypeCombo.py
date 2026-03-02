"""Delegate for editing stint types in the stint table."""

from PyQt6.QtWidgets import QStyledItemDelegate

from .helpers import (
    _find_view,
    create_editor,
    paint,
    set_editor_data,
    set_model_data,
    update_editor_geometry,
)


class StintTypeCombo(QStyledItemDelegate):
    """Combo-based stint type editor with optional DB updates."""

    createEditor = create_editor
    _find_view = _find_view
    updateEditorGeometry = update_editor_geometry
    paint = paint
    setEditorData = set_editor_data
    setModelData = set_model_data

    def __init__(self, parent=None, update_doc: bool = False, strategy_id: str | None = None) -> None:
        super().__init__(parent)
        self.update_doc = update_doc
        self.strategy_id = strategy_id
        self.items = [
            "", "Single", "Double", "Triple", "Quadruple", "Quintuple",
            "Sextuple", "Septuple", "Octuple", "Nonuple", "Decuple",
        ]
        self.lock_completed = False
