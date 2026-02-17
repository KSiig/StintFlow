"""
Table model for stint tracking data.

QAbstractTableModel implementation for displaying stint information.
Orchestrates data loading, editing, and display using separate processor modules.
"""

import copy

from PyQt6.QtCore import QAbstractTableModel, Qt, QModelIndex, pyqtSignal
from PyQt6.QtGui import QColor, QBrush

from ui.utilities import get_fonts, FONT, load_icon
from core.database import get_stints, get_event
from core.errors import log
from core.utilities import resource_path
from ui.components.stint_tracking import get_header_icon
from datetime import datetime, timedelta

from .TableRoles import TableRoles
from .table_constants import ColumnIndex, FULL_TIRE_SET, NO_TIRE_CHANGE
from .table_utils import is_completed_row
from .table_processors import (
    convert_stints_to_table,
    count_tire_changes,
    recalculate_tires_left,
    recalculate_stint_types,
    recalculate_tires_changed
)
from .stint_helpers import get_default_tire_dict

# Constants
DEFAULT_TIRE_COUNT = "0"
DEFAULT_RACE_LENGTH = "00:00:00"
HEADER_ICON_COLOR = "#FFFFFF"
VERTICAL_HEADER_START_INDEX = 1  # Row numbers are 1-indexed


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
        headers: list[dict],
        data: list[list] = None,
        tires: list[dict] = None,
        meta: list[dict] = None,
        mean_stint_time: timedelta = None
    ):
        """
        Initialize the table model.
        
        Args:
            selection_model: SelectionModel with current event/session selection
            headers: Column header definitions (list of dicts with 'title' and 'icon')
            data: Optional pre-populated display data
            tires: Optional pre-populated tire metadata
            meta: Optional pre-populated document metadata
            mean_stint_time: Optional mean stint time for calculations
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
            self._mean_stint_time = mean_stint_time or timedelta(0)
        else:
            self._data = []
            self._tires = []
            self._meta = []
            self._mean_stint_time = timedelta(0)
            self._load_data_from_database()
    
    def clone(self) -> 'TableModel':
        """
        Create a deep copy of this model.
        
        Returns:
            New TableModel instance with copied data
        """
        log('DEBUG', 'Cloning table model', category='table_model', action='clone')
        return TableModel(
            selection_model=self.selection_model,
            headers=copy.deepcopy(self.headers),
            data=copy.deepcopy(self._data),
            tires=copy.deepcopy(self._tires),
            meta=copy.deepcopy(self._meta),
            mean_stint_time=copy.deepcopy(self._mean_stint_time)
        )
    
    def update_data(self, data: list[list] = None, tires: list[dict] = None, mean_stint_time: timedelta = None) -> None:
        """
        Update model data and trigger view refresh.
        
        Args:
            data: Optional new display data (reloads from DB if not provided)
            tires: Optional new tire metadata
            mean_stint_time: Optional mean stint time for calculations
        """
        self.beginResetModel()
        
        if data is not None:
            self._data = data
            self._tires = tires or []
            self._mean_stint_time = mean_stint_time or timedelta(0)
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
            total_tires = str(event.get('tires', DEFAULT_TIRE_COUNT))
            starting_time = event.get('length', DEFAULT_RACE_LENGTH)
        else:
            total_tires = DEFAULT_TIRE_COUNT
            starting_time = DEFAULT_RACE_LENGTH
            log('WARNING', f'Event {self.selection_model.event_id} not found - using defaults',
                category='table_model', action='load_data')
        
        # Get stints for current session
        stints = get_stints(self.selection_model.session_id)
        stints = sorted(stints, key=self._parse_pit_time, reverse=True)
        
        # Extract tire and meta data
        self._tires = [stint.get("tire_data", {}) for stint in stints]
        self._meta = [{"id": stint.get("_id"), "excluded": True} for stint in stints]
        
        # Convert stints to table rows using processor
        rows, mean_stint_time, last_tire_change = convert_stints_to_table(
            stints, total_tires, starting_time, count_tire_changes
        )
        self._data = rows
        self._mean_stint_time = mean_stint_time
        
        # Ensure _tires array matches _data length
        i = 0 if last_tire_change is NO_TIRE_CHANGE else 1

        while len(self._tires) < len(self._data):
            tires_changed = bool(i % 2)  # Alternate between no change and full change for new rows
            self._tires.append(get_default_tire_dict(not tires_changed))
            i += 1
        
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

    def _parse_pit_time(self, stint: dict) -> datetime:
        """Parse a stint pit end time into a sortable datetime value."""
        pit_time_str = stint.get('pit_end_time', '00:00:00')
        pit_time = datetime.strptime(pit_time_str, "%H:%M:%S").time()
        return datetime.combine(datetime.min, pit_time)
    
    def set_editable(self, editable: bool, partial: bool = False) -> None:
        """
        Configure edit mode.
        
        Args:
            editable: Whether cells can be edited
            partial: If True, only "Completed" rows are editable
        """
        self.editable = editable
        self.partial = partial
    
    def get_all_data(self) -> tuple[list[list], list[dict], timedelta]:
        """
        Get all model data.
        
        Returns:
            Tuple of (display_data, tire_metadata, mean_stint_time)
        """
        return self._data, self._tires, self._mean_stint_time
    
    # Qt Model Interface Methods
    
    def rowCount(self, parent: QModelIndex = None) -> int:
        """
        Return number of rows in model.
        
        Args:
            parent: Parent index (unused for table models)
            
        Returns:
            Number of rows
        """
        if parent is None:
            parent = QModelIndex()
        return len(self._data)
    
    def columnCount(self, parent: QModelIndex = None) -> int:
        """
        Return number of columns in model.
        
        Args:
            parent: Parent index (unused for table models)
            
        Returns:
            Number of columns, or 0 if no data
        """
        if parent is None:
            parent = QModelIndex()
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

        elif role == Qt.ItemDataRole.BackgroundRole:
            # Use row meta to determine excluded state and tint entire row
            meta = self._meta[row] if row < len(self._meta) else None
            if isinstance(meta, dict) and meta.get('excluded'):
                return QColor('#281F23')
        
        elif role == Qt.ItemDataRole.FontRole:
            return get_fonts(FONT.text_table_cell)
        
        elif role == Qt.ItemDataRole.TextAlignmentRole:
            return  Qt.AlignmentFlag.AlignVCenter
        
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
        if not index.isValid() or role not in (Qt.ItemDataRole.EditRole, TableRoles.TiresRole, TableRoles.MetaRole):
            return False
        
        row = index.row()
        col = index.column()
        
        if role == Qt.ItemDataRole.EditRole:
            self._data[row][col] = value
        
        elif role == TableRoles.TiresRole:
            while row >= len(self._tires):
                self._tires.append({})
            self._tires[row] = value
            # Update tire change count
            tires_changed = sum(value.get('tires_changed', {}).values())
            self._data[row][ColumnIndex.TIRES_CHANGED] = str(tires_changed)

        elif role == TableRoles.MetaRole:
            # Ensure meta list is large enough and store value
            while row >= len(self._meta):
                self._meta.append({})
            self._meta[row] = value
        
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
        
        # Determine if this cell should be editable
        editable_columns = {
            ColumnIndex.STINT_TYPE,
            ColumnIndex.TIRES_CHANGED
        }
        is_editable = self.editable and index.column() in editable_columns and (
            not self.partial or is_completed_row(self._data, index.row())
        )
        
        if is_editable:
            return self._get_editable_flags()
        
        return Qt.ItemFlag.NoItemFlags
    
    def _get_editable_flags(self) -> Qt.ItemFlag:
        """Return standard flags for editable cells."""
        return (
            Qt.ItemFlag.ItemIsSelectable |
            Qt.ItemFlag.ItemIsEnabled |
            Qt.ItemFlag.ItemIsEditable
        )
    
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
            role: Data role (DisplayRole for text, DecorationRole for icon)
            
        Returns:
            Header label, icon, or None
        """
        if orientation == Qt.Orientation.Horizontal and section < len(self.headers):
            if role == Qt.ItemDataRole.DisplayRole:
                return self.headers[section]
            elif role == Qt.ItemDataRole.DecorationRole:
                icon_file = get_header_icon(section)
                icon_path = f"resources/icons/table_headers/{icon_file}"
                return load_icon(icon_path, color=HEADER_ICON_COLOR)
            elif role == Qt.ItemDataRole.TextAlignmentRole:
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        
        elif orientation == Qt.Orientation.Vertical:
            if role == Qt.ItemDataRole.DisplayRole:
                return section + VERTICAL_HEADER_START_INDEX
            elif role == Qt.ItemDataRole.TextAlignmentRole:
                return Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter
        
        return None
