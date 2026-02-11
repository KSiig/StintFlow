"""
Tire change combo delegate for stint table.

Custom delegate for editing tire changes with a popup selector.
"""

import copy
from PyQt6.QtWidgets import (
    QWidget, QHBoxLayout, QPushButton,
    QGridLayout, QSizePolicy, QAbstractItemView, QStyledItemDelegate, QFrame, QVBoxLayout
)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QIcon, QPixmap

from core.utilities import resource_path
from core.database import update_strategy, update_stint
from core.errors import log
from ui.models.TableRoles import TableRoles
from ui.models.stint_helpers import sanitize_stints
from ui.components.common import DropdownButton, ConfigButton
from ui.utilities import load_icon


class TireComboDelegate(QStyledItemDelegate):
    """
    Delegate for editing tire changes in the stint table.
    
    Shows a button displaying the number of tires changed. When clicked,
    opens a popup allowing selection of which tires to change and their compounds.
    """
    
    def __init__(self, parent=None, update_doc: bool = False, strategy_id: str = None):
        """
        Initialize tire combo delegate.
        
        Args:
            parent: Parent widget
            update_doc: Whether to update database on changes
            strategy_id: MongoDB strategy ID (required if update_doc=True)
        """
        super().__init__(parent)
        self.update_doc = update_doc
        self.strategy_id = strategy_id
        self.tires_changed = "0"
        self.setObjectName("TireComboDelegate")
    
    def createEditor(self, parent, option, index):
        """Create custom editor widget with button and popup."""
        editor = QWidget(parent)
        editor.setAutoFillBackground(True)
        editor.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Maximum
        )
        # Set the editor's palette to match the cell's background
        editor.setPalette(option.palette)
        # Explicitly set background color via stylesheet (only for the editor, not children)
        bg_color = option.palette.color(option.palette.ColorRole.Base).name()
        editor.setStyleSheet(f"QWidget#TireComboDelegate {{ background-color: {bg_color}; }}")
        editor.setObjectName("TireComboDelegate")
        layout = QHBoxLayout(editor)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create button showing tire count
        btn = ConfigButton(parent=editor, width_type="third")
        btn.setObjectName("TirePicker")
        btn.setSizePolicy(
            QSizePolicy.Policy.Maximum,
            QSizePolicy.Policy.Maximum
        )
        self._update_button_text(btn, index)
        layout.addWidget(btn)
        
        # Create popup for tire selection
        popup = TirePopup(editor)
        
        def show_popup():
            """Show popup at correct position below cell."""
            view = self._find_view(editor)
            if not view:
                return
            
            # Position popup at bottom-left of the button
            pos = btn.mapToGlobal(btn.rect().bottomLeft())
            pos.setY(pos.y() + 4)
            
            # Load current tire values
            value = index.data(TableRoles.TiresRole)
            popup.set_values(value)
            
            popup.move(pos)
            popup.show()
        
        # Connect signals
        popup.dataChanged.connect(lambda: self.commitData.emit(editor))
        btn.clicked.connect(show_popup)
        
        # Store references for later access
        editor.popup = popup
        editor.btn = btn

        if not self.strategy_id:
            QTimer.singleShot(0, show_popup) 

        return editor
    
    def setEditorData(self, editor, index):
        """Load data into editor from model."""
        editor.blockSignals(True)
        self.tires_changed = index.data()
        self._update_button_text(editor.btn, index)
        editor.blockSignals(False)
    
    def setModelData(self, editor, model, index):
        """Save data from editor to model."""
        # Get new values from popup
        values = editor.popup.values()
        values_lowered = {k.lower(): v.lower() for k, v in values.items()}
        
        # Get current tire data
        old_value = model.data(index, TableRoles.TiresRole)
        new_value = copy.deepcopy(old_value)
        
        # Update tire data based on selections
        for tire, compound in values_lowered.items():
            new_value['tires_changed'][tire] = bool(compound)
            if compound:
                new_value[tire.lower()]['outgoing']['compound'] = compound
        
        # Check if anything changed
        if new_value == old_value:
            return  # Prevents duplicate trigger
        
        # Update model
        model.setData(index, new_value, TableRoles.TiresRole)
        model._recalculate_tires_left()
        
        # Update database if enabled
        if self.update_doc and self.strategy_id:
            row_data, tire_data, _ = model.get_all_data()
            sanitized_data = sanitize_stints(row_data, tire_data)
            update_strategy(self.strategy_id, sanitized_data)
        elif self.update_doc:
            row_data, tire_data, _ = model.get_all_data()
            sanitized_data = sanitize_stints(row_data, tire_data)
            stint_id = model.data(index, TableRoles.MetaRole)['id']
            row = sanitized_data['tires'][index.row()]
            update_stint(stint_id, row)
        else:
            log('INFO', 'Database update skipped (update_doc=False or no strategy_id)',
                category='tire_combo_delegate', action='set_model_data')

    def updateEditorGeometry(self, editor, option, index):
        """Ensure the editor fills the full cell rect."""
        editor.setGeometry(option.rect)
    
    def _update_button_text(self, btn: QPushButton, index):
        """Update button text showing tire count."""
        tire_data = index.data(TableRoles.TiresRole)
        if tire_data:
            tires_changed = sum(tire_data['tires_changed'].values())
        else:
            tires_changed = 0
        
        btn.setText(str(tires_changed))
    
    def _find_view(self, widget) -> QAbstractItemView:
        """Find parent QAbstractItemView for positioning popup."""
        while widget:
            if isinstance(widget, QAbstractItemView):
                return widget
            widget = widget.parent()
        return None


class TirePopup(QWidget):
    """
    Popup widget for selecting tire changes.
    
    Shows combo boxes for each tire (FL, FR, RL, RR) with compound options,
    plus buttons for quickly setting all tires.
    """
    
    dataChanged = pyqtSignal()
    
    def __init__(self, parent=None):
        """Initialize tire popup widget."""
        super().__init__(parent, Qt.WindowType.Popup)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint, True)
        self.setWindowFlag(Qt.WindowType.NoDropShadowWindowHint, True)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)

        container = QFrame(self)
        container.setObjectName("TirePopupContainer")

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.setSpacing(0)
        outer_layout.addWidget(container)

        layout = QGridLayout(container)
        
        SIZE_BTN = QSize(36, 36)
        SIZE_ICON = QSize(24, 24)
        
        # Create quick-set buttons
        btn_x = QPushButton()
        btn_x.setIcon(QIcon(load_icon('resources/icons/tires/x.svg', size=SIZE_ICON.height() + 4, color="#D1D5DC")))
        btn_medium = QPushButton()
        medium_pixmap = QPixmap(resource_path('resources/icons/tires/medium.png'))
        btn_medium.setIcon(QIcon(medium_pixmap.scaledToHeight(SIZE_ICON.height(), Qt.TransformationMode.SmoothTransformation)))
        btn_wet = QPushButton()
        wet_pixmap = QPixmap(resource_path('resources/icons/tires/wet.png'))
        btn_wet.setIcon(QIcon(wet_pixmap.scaledToHeight(SIZE_ICON.height(), Qt.TransformationMode.SmoothTransformation)))
        
        # Connect quick-set buttons
        btn_x.clicked.connect(lambda: self.set_all_tires(None))
        btn_medium.clicked.connect(lambda: self.set_all_tires("medium"))
        btn_wet.clicked.connect(lambda: self.set_all_tires("wet"))
        
        # Style quick-set buttons
        for btn in (btn_medium, btn_wet, btn_x):
            btn.setFixedSize(SIZE_BTN)
            btn.setIconSize(SIZE_ICON)
            btn.setObjectName("TirePopupQuickSetButton")

        btn_x.setIconSize(QSize(SIZE_ICON.width() + 3, SIZE_ICON.height() + 3))

        # Add quick-set buttons to layout
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(0)
        btn_layout.addWidget(btn_x)
        btn_layout.addWidget(btn_medium)
        btn_layout.addWidget(btn_wet)
        btn_layout.addStretch()
        layout.addLayout(btn_layout, 0, 1)
        
        # Create tire selection combos
        self.boxes = {}
        dropdown_items = ["", "Medium", "Wet", "Used medium", "Used wet"]
        for i, tire in enumerate(["FL", "FR", "RL", "RR"]):
            row = (i // 2) + 1  # 0,0,1,1 -> 1,1,2,2
            col = (i % 2) * 2   # 0,2,0,2
            
            # label = QLabel(tire)
            cb = DropdownButton(
                items=dropdown_items,
                current_value="",
                parent=container,
                button_object_name="TirePopupDropdown",
            )
            cb.valueChanged.connect(lambda _: self.dataChanged.emit())
            
            # layout.addWidget(label, row, col)
            layout.addWidget(cb, row, col + 1)
            
            self.boxes[tire] = cb
    
    def set_values(self, data: dict):
        """
        Load tire data into combo boxes.
        
        Args:
            data: Tire data dict with 'tires_changed' and tire compound info
        """
        for tire in self.boxes:
            tire_changed = data['tires_changed'][tire.lower()]
            tire_compound = data[tire.lower()]['outgoing']['compound'].capitalize()
            
            if tire_changed:
                self.boxes[tire].set_value(tire_compound)
            else:
                self.boxes[tire].set_value("")
    
    def values(self) -> dict:
        """
        Get current values from combo boxes.
        
        Returns:
            Dict mapping tire names to selected compounds
        """
        return {k: v.get_value() for k, v in self.boxes.items()}
    
    def set_all_tires(self, compound: str = None):
        """
        Set all tires to the same compound.
        
        Args:
            compound: Compound name ("medium", "wet") or None to clear
        """
        for tire in self.boxes:
            if compound:
                self.boxes[tire].set_value(compound.capitalize())
            else:
                self.boxes[tire].set_value("")
            self.dataChanged.emit()
