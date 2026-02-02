"""
Table model for stint tracking data.

QAbstractTableModel implementation for displaying stint information.
Orchestrates data loading, editing, and display using separate processor modules.
"""

import copy

from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, pyqtSignal

from ui.utilities import get_fonts, FONT
from core.database import get_stints, get_event
from core.errors import log

from .TableRoles import TableRoles
from .table_constants import ColumnIndex
from .table_utils import create_table_row, is_completed_row
from .table_processors import (
    convert_stints_to_table,
    count_tire_changes,
    recalculate_tires_left,
    recalculate_stint_types,
    recalculate_tires_changed
)
from .stint_helpers import get_default_tire_dict


class TableModel(QAbstractTableModel):
    """
    Model for stint tracking table data.
    
    Manages display data (_data), tire metadata (_tires), and document IDs (_meta).
    Handles complex stint type calculations and tire management logic.
    """
    
    # Signal emitted when editors need refreshing (for persistent editors)
    editorsNeedRefresh = pyqtSignal()
    
    def __init__(
        self,
        selection_model,
        headers: list[str],
        data: list[list] = None,
        tires: list[dict] = None,
        meta: list[dict] = None
    ):
        """
        Initialize the table model.
        
        Args:
            selection_model: SelectionModel with current event/session selection
            headers: Column header names
            data: Optional pre-populated display data
            tires: Optional pre-populated tire metadata
            meta: Optional pre-populated document metadata
        """
        super().__init__()
        
        self.selection_model = selection_model
        self.headers = headers
        self.editable = False
        self.partial = False
        
        # Initialize data structures
        if data is not None:
            self._data = data
            self._tires = tires or []
            self._meta = meta or []
        else:
            self._data = []
            self._tires = []
            self._meta = []
            self._load_data_from_database()
    
    def clone(self):
        """
        Create a deep copy of this model.
        
        Returns:
            New TableModel instance with copied data
        """
        return TableModel(
            selection_model=self.selection_model,
            headers=copy.deepcopy(self.headers),
            data=copy.deepcopy(self._data),
            tires=copy.deepcopy(self._tires),
            meta=copy.deepcopy(self._meta)
        )
    
    def update_data(self, data: list[list] = None, tires: list[dict] = None) -> None:
        """
        Update model data and trigger view refresh.
        
        Args:
            data: Optional new display data (reloads from DB if not provided)
            tires: Optional new tire metadata
        """
        self.beginResetModel()
        
        if data is not None:
            self._data = data
            self._tires = tires or []
            self._repaint_table()
        else:
            self._load_data_from_database()
        
        self.endResetModel()
    
    def _load_data_from_database(self) -> None:
        """Load stint data from database and convert to table format."""
        # Validate selection
        if not self.selection_model.event_id or not self.selection_model.session_id:
            log('WARNING', 'No event or session selected - cannot load data',
                category='table_model', action='load_data')
            return
        
        log('DEBUG', f'Loading data for event {self.selection_model.event_id}, '
                    f'session {self.selection_model.session_id}',
            category='table_model', action='load_data')
        
        # Get event info for tire count and race length
        event = get_event(self.selection_model.event_id)
        if event:
            total_tires = str(event.get('tires', '0'))
            starting_time = event.get('length', '00:00:00')
        else:
            total_tires = "0"
            starting_time = "00:00:00"
            log('WARNING', f'Event {self.selection_model.event_id} not found - using defaults',
                category='table_model', action='load_data')
        
        # Get stints for current session
        stints = get_stints(self.selection_model.session_id)
        
        # Extract tire and meta data
        self._tires = [stint.get("tire_data", {}) for stint in stints]
        self._meta = [{"id": stint.get("_id")} for stint in stints]
        
        # Convert stints to table rows using processor
        self._data = convert_stints_to_table(
            stints, total_tires, starting_time, count_tire_changes
        )
        
        # Ensure _tires array matches _data length
        while len(self._tires) < len(self._data):
            self._tires.append(get_default_tire_dict(True))
        
        # Calculate stint types and tire counts
        self._recalculate_stint_types()
        self._repaint_table()
    
    def _recalculate_tires_left(self) -> None:
        """Recalculate remaining tires for all rows based on tire changes."""
        recalculate_tires_left(
            self._data,
            self._tires,
            self.selection_model.event_id,
            self._recalculate_stint_types
        )
    
    def _recalculate_tires_changed(self, index: QModelIndex, old_value: str) -> None:
        """
        Recalculate tire changes after stint type edit.
        
        Args:
            index: Index of edited cell
            old_value: Previous stint type value
        """
        recalculate_tires_changed(
            self._data,
            self._tires,
            index.row(),
            old_value,
            self.rowCount(),
            self._recalculate_tires_left
        )
    
    def _recalculate_stint_types(self) -> None:
        """Recalculate stint types for all rows based on tire changes."""
        recalculate_stint_types(
            self._data,
            self.index,
            self.rowCount,
            self.editorsNeedRefresh.emit,
            self.dataChanged.emit,
            self._repaint_table
        )
    
    def _repaint_table(self) -> None:
        """Emit dataChanged signal for entire table."""
        if self.rowCount() > 0 and self.columnCount() > 0:
            top_left = self.index(0, 0)
            bottom_right = self.index(self.rowCount() - 1, self.columnCount() - 1)
            self.dataChanged.emit(top_left, bottom_right, [])
    
    def set_editable(self, editable: bool, partial: bool = False) -> None:
        """
        Configure edit mode.
        
        Args:
            editable: Whether cells can be edited
            partial: If True, only "Completed" rows are editable
        """
        self.editable = editable
        self.partial = partial
    
    def get_all_data(self) -> tuple[list[list], list[dict]]:
        """
        Get all model data.
        
        Returns:
            Tuple of (display_data, tire_metadata)
        """
        return self._data, self._tires
    
    # Qt Model Interface Methods
    
    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return number of rows in model."""
        return len(self._data)
    
    def columnCount(self, parent: QModelIndex = QModelIndex()) -> int:
        """Return number of columns in model."""
        return len(self._data[0]) if self._data else 0
    
    def data(self, index: QModelIndex, role: int = Qt.ItemDataRole.DisplayRole):
        """
        Retrieve data for a specific cell and role.
        
        Args:
            index: Cell index
            role: Data role (DisplayRole, FontRole, TiresRole, etc.)
            
        Returns:
            Data for the requested role, or None if invalid
        """
        if not index.isValid():
            return None
        
        row = index.row()
        col = index.column()
        
        # Bounds checking
        if row >= len(self._data) or (self._data and col >= len(self._data[row])):
            return None
        
        if role == Qt.ItemDataRole.DisplayRole:
            return self._data[row][col]
        
        elif role == Qt.ItemDataRole.FontRole:
            return get_fonts(FONT.text_table_cell)
        
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter
        
        elif role == TableRoles.TiresRole:
            return self._tires[row] if row < len(self._tires) else None
        
        elif role == TableRoles.MetaRole:
            return self._meta[row] if row < len(self._meta) else None
        
        return None
    
    def setData(
        self,
        index: QModelIndex,
        value,
        role: int = Qt.ItemDataRole.EditRole
    ) -> bool:
        """
        Update data for a specific cell.
        
        Args:
            index: Cell index
            value: New value
            role: Data role (EditRole or TiresRole)
            
        Returns:
            True if data was updated, False otherwise
        """
        if not index.isValid() or role not in (Qt.ItemDataRole.EditRole, TableRoles.TiresRole):
            return False
        
        row = index.row()
        col = index.column()
        
        if role == Qt.ItemDataRole.EditRole:
            self._data[row][col] = value
        
        elif role == TableRoles.TiresRole:
            self._tires[row] = value
            # Update tire change count
            tires_changed = sum(value.get('tires_changed', {}).values())
            self._data[row][ColumnIndex.TIRES_CHANGED] = str(tires_changed)
        
        # Notify view
        self.dataChanged.emit(
            index,
            index,
            [Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.EditRole]
        )
        
        return True
    
    def flags(self, index: QModelIndex) -> Qt.ItemFlag:
        """
        Return item flags for a cell.
        
        Args:
            index: Cell index
            
        Returns:
            Qt.ItemFlag indicating cell capabilities
        """
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags
        
        if self.editable and self.partial:
            # Only completed rows editable
            if is_completed_row(self._data, index.row()):
                return (
                    Qt.ItemFlag.ItemIsSelectable |
                    Qt.ItemFlag.ItemIsEnabled |
                    Qt.ItemFlag.ItemIsEditable
                )
            else:
                return Qt.ItemFlag.NoItemFlags
        
        elif self.editable:
            # All rows editable
            return (
                Qt.ItemFlag.ItemIsSelectable |
                Qt.ItemFlag.ItemIsEnabled |
                Qt.ItemFlag.ItemIsEditable
            )
        
        else:
            # No editing
            return Qt.ItemFlag.NoItemFlags
    
    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole
    ):
        """
        Return header data.
        
        Args:
            section: Row/column index
            orientation: Horizontal or Vertical
            role: Data role
            
        Returns:
            Header label or None
        """
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Orientation.Horizontal:
                return self.headers[section] if section < len(self.headers) else None
            elif orientation == Qt.Orientation.Vertical:
                return section + 1  # Row numbers (1-indexed)
        
        return None
