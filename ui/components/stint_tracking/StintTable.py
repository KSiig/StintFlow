"""
Stint table component for displaying race stint data.

A QTableView-based component that shows stint information including:
- Stint type, driver, status
- Pit times, tire changes
- Stint duration

Supports optional editing mode with tire combo delegates.
"""

from PyQt6.QtWidgets import (
    QTableView,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QAbstractButton,
    QAbstractItemView,
    QSizePolicy,
    QHeaderView
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon

from ui.models import ModelContainer
from ui.utilities import get_fonts, FONT
from core.errors import log
from core.utilities import resource_path

from .constants import (
    TABLE_HEADERS,
    COLUMN_WIDTHS,
    VERTICAL_HEADER_WIDTH,
    VERTICAL_HEADER_LABEL
)


class StintTable(QWidget):
    """
    Table view for displaying racing stint data.
    
    Features:
    - Auto-updates when session changes (if auto_update=True)
    - Optional editor mode for tire changes
    - Styled table with custom headers and column widths
    - No horizontal scrollbar (fixed column layout)
    """
    
    def __init__(
        self,
        models: ModelContainer,
        focus: bool = False,
        auto_update: bool = True,
        allow_editors: bool = False
    ):
        """
        Initialize the stint table.
        
        Args:
            models: Container with selection_model and table_model
            focus: Whether table accepts keyboard focus and selection (default: False)
            auto_update: Whether to refresh when session changes (default: True)
            allow_editors: Whether to enable tire combo editors (default: False)
        """
        super().__init__()
        
        self.selection_model = models.selection_model
        self.table_model = models.table_model
        self._column_count = 0
        
        # Load stylesheet
        self._load_stylesheet()
        
        # Create table
        self.table = self._create_table(focus)
        
        # Setup layout
        container = QHBoxLayout(self)
        container.addWidget(self.table)
        
        # Configure table model (if available)
        if self.table_model is not None:
            self.table_model.update_data()
            self.refresh_table()  # Initial load
            
            # Setup editors if needed
            if allow_editors:
                self._setup_editors()
            else:
                self.table_model.editorsNeedRefresh.connect(self._refresh_editors)
        else:
            log('WARNING', 'TableModel not available - table will be empty',
                category='stint_table', action='init')
        
        # Setup auto-update
        if auto_update:
            self.selection_model.sessionChanged.connect(self.refresh_table)
    
    def _load_stylesheet(self) -> None:
        """Load QSS stylesheet for stint table."""
        try:
            stylesheet_path = resource_path('resources/styles/stint_tracker.qss')
            with open(stylesheet_path, 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            log('WARNING', f'Stylesheet not found: {stylesheet_path}',
                category='stint_table', action='load_stylesheet')
        except Exception as e:
            log('ERROR', f'Failed to load stylesheet: {e}',
                category='stint_table', action='load_stylesheet')
    
    def _create_table(self, focus: bool) -> QTableView:
        """
        Create and configure the table view.
        
        Args:
            focus: Whether table accepts keyboard focus and selection
            
        Returns:
            Configured QTableView instance
        """
        table = QTableView(self)
        table.setShowGrid(False)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        table.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Expanding
        )
        table.setObjectName("StintsTable")
        
        # Configure focus and selection
        if not focus:
            table.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
            table.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        
        # Setup headers
        self._setup_vertical_header(table)
        self._setup_horizontal_header(table)
        
        return table
    
    def _setup_vertical_header(self, table: QTableView) -> None:
        """
        Configure vertical header (row numbers).
        
        Args:
            table: Table view to configure
        """
        vh = table.verticalHeader()
        
        # Get fonts for styling
        font_table_cell = get_fonts(FONT.text_table_cell)
        font_table_header = get_fonts(FONT.header_table)
        
        vh.setStyleSheet(
            f"QHeaderView::section {{ "
            f"font-family: {font_table_cell.family()}; "
            f"font-size: {font_table_cell.pointSize()}pt; "
            f"}}"
        )
        vh.setFixedWidth(VERTICAL_HEADER_WIDTH)
        vh.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Configure corner button with "Stint no." label
        corner = table.findChild(QAbstractButton)
        if corner:
            corner.setText("")
            corner.setIcon(QIcon())
            
            layout = QVBoxLayout()
            layout.setContentsMargins(2, 2, 2, 2)
            layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            
            label = QLabel(VERTICAL_HEADER_LABEL)
            label.setAlignment(Qt.AlignmentFlag.AlignHCenter)
            label.setFont(font_table_header)
            
            corner.setLayout(layout)
            layout.addWidget(label)
            corner.setFixedWidth(VERTICAL_HEADER_WIDTH)
    
    def _setup_horizontal_header(self, table: QTableView) -> None:
        """
        Configure horizontal header (column names).
        
        Args:
            table: Table view to configure
        """
        hh = table.horizontalHeader()
        font_table_header = get_fonts(FONT.header_table)
        hh.setFont(font_table_header)
    
    def _setup_editors(self) -> None:
        """Enable editing mode with tire combo delegates."""
        if self.table.model() is None:
            log('WARNING', 'Cannot setup editors - no model available',
                category='stint_table', action='setup_editors')
            return
        
        self.table.model().set_editable(True, True)
        
        # TODO: Import and set TireComboDelegate when migrated
        # from .delegates import TireComboDelegate
        # self.table.setItemDelegateForColumn(
        #     4,  # Tires changed column
        #     TireComboDelegate(self.table, update_doc=True)
        # )
        log('WARNING', 'TireComboDelegate not yet migrated - editors disabled',
            category='stint_table', action='setup_editors')
    
    def _refresh_editors(self) -> None:
        """
        Refresh persistent editors based on cell content.
        
        Opens editors for non-empty cells in stint_type column,
        closes editors for empty cells.
        """
        if self.table.model() is None:
            return
        
        for row in range(self.table.model().rowCount()):
            index = self.table.model().index(row, 0)  # stint_type column
            cell_text = str(index.data())
            
            if cell_text:  # Non-empty → open editor
                self.table.openPersistentEditor(index)
            else:  # Empty → close editor
                self.table.closePersistentEditor(index)
    
    def refresh_table(self) -> None:
        """
        Refresh table data and column configuration.
        
        Updates model data and reconfigures columns if column count changed.
        """
        # Early return if no table_model available
        if self.table_model is None:
            return
        
        # Check if columns need reconfiguration
        if self.table.model():
            column_count = self.table.model().columnCount()
            if self._column_count != column_count:
                self._set_column_widths()
        
        # Set model on first load
        if self.table.model() is None:
            self.table.setModel(self.table_model)
            if self.table.model() is not None:  # Verify model was set successfully
                self._column_count = self.table.model().columnCount()
                self._set_column_widths()
        else:
            # Update existing model
            self.table_model.update_data()
    
    def _set_column_widths(self) -> None:
        """Configure fixed column widths based on COLUMN_WIDTHS constant."""
        hh = self.table.horizontalHeader()
        
        for col, width in COLUMN_WIDTHS.items():
            hh.setSectionResizeMode(col, QHeaderView.ResizeMode.Fixed)
            self.table.setColumnWidth(col, width)
        
        # Calculate minimum table width
        min_width = hh.length() + VERTICAL_HEADER_WIDTH + 20  # Extra padding
        self.table.setMinimumWidth(min_width)
        
        # Disable header interactions
        hh.setSectionsMovable(False)
        hh.setCascadingSectionResizes(False)
        hh.setHighlightSections(False)
