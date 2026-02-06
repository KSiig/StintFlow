"""
Stint type combo delegate for stint table.

Custom delegate for editing stint types with dropdown.
"""

from PyQt6.QtWidgets import QStyledItemDelegate, QWidget, QHBoxLayout, QAbstractItemView
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFontMetrics

from core.database import update_strategy
from core.errors import log
from ui.models.stint_helpers import sanitize_stints
from ui.utilities import get_fonts, FONT
from ui.components.common import DropdownButton


class StintTypeCombo(QStyledItemDelegate):
    """
    Delegate for editing stint types in the stint table.
    
    Shows a combo box with predefined stint type options (Single, Double, etc.).
    Disabled for empty cells (pending stints).
    """
    
    def __init__(self, parent=None, update_doc: bool = False, strategy_id: str = None):
        """
        Initialize stint type combo delegate.
        
        Args:
            parent: Parent widget
            update_doc: Whether to update database on changes
            strategy_id: MongoDB strategy ID (required if update_doc=True)
        """
        super().__init__(parent)
        self.update_doc = update_doc
        self.strategy_id = strategy_id
        self.items = [
            "", "Single", "Double", "Triple", "Quadruple", "Quintuple",
            "Sextuple", "Septuple", "Octuple", "Nonuple", "Decuple"
        ]
    
    def createEditor(self, parent, option, index):
        """Create custom editor widget with button and popup."""
        editor = QWidget(parent)
        editor.setAutoFillBackground(True)
        # Set the editor's palette to match the cell's background
        editor.setPalette(option.palette)
        # Explicitly set background color via stylesheet (only for the editor, not children)
        bg_color = option.palette.color(option.palette.ColorRole.Base).name()
        editor.setStyleSheet(f"QWidget#StintTypeComboEditor {{ background-color: {bg_color}; }}")
        editor.setObjectName("StintTypeComboEditor")
        
        # Create layout
        layout = QHBoxLayout(editor)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create dropdown button with stint type options
        dropdown = DropdownButton(
            items=self.items,
            current_value=str(index.data()) or "",
            parent=editor
        )
        dropdown.btn.setFont(get_fonts(FONT.table_cell))
        dropdown.btn.setStyleSheet("text-align: left; padding-left: 8px;")
        
        # Disable if empty (pending stint)
        current_text = str(index.data())
        if current_text == "":
            dropdown.btn.setEnabled(False)
        
        # Connect signal to commit data
        dropdown.valueChanged.connect(lambda: self.commitData.emit(editor))
        
        layout.addWidget(dropdown)
        
        # Store reference
        editor.dropdown = dropdown
        
        return editor
    
    def _find_view(self, widget) -> QAbstractItemView:
        """Find parent QAbstractItemView for positioning popup."""
        while widget:
            if isinstance(widget, QAbstractItemView):
                return widget
            widget = widget.parent()
        return None
    
    def sizeHint(self, option, index):
        """Return size hint for the editor, 50px wider than default."""
        hint = super().sizeHint(option, index)
        return QSize(hint.width() + 50, hint.height())
    
    def setEditorData(self, editor, index):
        """Load data into editor from model."""
        editor.dropdown.set_value(str(index.data()))
    
    def setModelData(self, editor, model, index):
        """Save data from editor to model."""
        old_value = model.data(index, Qt.ItemDataRole.DisplayRole)
        new_value = editor.dropdown.get_value()
        
        # Check if anything changed
        if new_value == old_value:
            return  # Prevents duplicate trigger
        
        # Update model
        model.setData(index, new_value)
        model._recalculate_tires_changed(index, old_value)
        
        # Update database if enabled
        if self.update_doc and self.strategy_id:
            row_data, tire_data = model.get_all_data()
            sanitized_data = sanitize_stints(row_data, tire_data)
            update_strategy(self.strategy_id, sanitized_data)
        else:
            log('DEBUG', 'Database update skipped (update_doc=False or no strategy_id)',
                category='stint_type_combo', action='set_model_data')
