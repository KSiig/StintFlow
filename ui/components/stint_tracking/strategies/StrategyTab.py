"""
Strategy display tab.

Shows an existing strategy with editable stint table.
"""

from datetime import timedelta
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from core.errors import log, log_exception
from core.utilities import resource_path
from ui.models import TableModel, SelectionModel, ModelContainer
from ui.models.table_constants import ColumnIndex
from ui.models.mongo_docs_to_rows import mongo_docs_to_rows
from ..widgets import StintTable
from ..delegates import TireComboDelegate, StintTypeCombo
from .StrategySettings import StrategySettings


class StrategyTab(QWidget):
    """
    Tab displaying an existing race strategy.
    
    Each tab has its own independent TableModel clone to avoid interference
    with the main stint tracker or other strategy tabs.
    """
    
    def __init__(self, strategy: dict, table_model: TableModel, selection_model: SelectionModel):
        """
        Initialize the strategy tab.
        
        Args:
            strategy: Strategy document with '_id', 'name', 'model_data'
            table_model: Main TableModel to clone for independent state
            selection_model: SelectionModel for session tracking
        """
        super().__init__()
        
        self.strategy = strategy
        self.strategy_id = strategy.get('_id')
        self.strategy_name = strategy.get('name', 'Unnamed Strategy')
        self.selection_model = selection_model
        
        # Clone table model for independent state
        self.table_model = table_model.clone()
        
        self._setup_styles()
        self._setup_ui()
        self._load_strategy_data()

    def _setup_styles(self) -> None:
        """Load and apply strategy tab stylesheet."""
        try:
            with open(resource_path('resources/styles/strategy_tab.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            log('WARNING', 'Strategy tab stylesheet not found', 
                category='strategy_tab', action='load_stylesheet')
    
    def _setup_ui(self):
        """Set up the UI with editable stint table."""
        try:
            layout = QHBoxLayout(self)
            layout.setContentsMargins(0, 0, 0, 0)

            models = ModelContainer(
                selection_model=self.selection_model,
                table_model=self.table_model
            )

            # StrategySettings component for top half
            strategy_settings = StrategySettings(self, models)
            strategy_settings.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            layout.addWidget(strategy_settings, stretch=1)

            # Create StintTable with editing enabled
            self.stint_table = StintTable(
                models=models,
                focus=True,
                auto_update=False,
                allow_editors=False
            )
            # Stint table fills bottom half
            layout.addWidget(self.stint_table, stretch=1)
            
            log('DEBUG', f'Strategy tab UI created: {self.strategy_name}',
                category='strategy_tab', action='setup_ui')
        
        except Exception as e:
            log_exception(e, 'Failed to setup StrategyTab UI',
                         category='strategy_tab', action='setup_ui')
    
    def _load_strategy_data(self):
        """Load strategy stints from MongoDB and populate table."""
        try:
            # Get model_data from strategy document
            model_data = self.strategy.get('model_data', {})
            stints = model_data.get('rows', [])
            tires = model_data.get('tires', [])
            mean_stint_time_seconds = model_data.get('mean_stint_time_seconds', 0)
            
            if not stints:
                log('INFO', f'No stints in strategy {self.strategy_name}',
                    category='strategy_tab', action='load_strategy_data')
                return
            
            # Convert MongoDB documents to table rows
            rows = mongo_docs_to_rows(stints)
            
            # Update table model with strategy data (including tire metadata)
            self.table_model.update_data(data=rows, tires=tires, mean_stint_time=timedelta(seconds=mean_stint_time_seconds))

            # Set custom delegates with strategy_id for database updates
            self._setup_strategy_delegates()
            
            log('DEBUG', f'Loaded {len(rows)} stints for strategy {self.strategy_name}',
                category='strategy_tab', action='load_strategy_data')
            
            # Open persistent editors for editable columns
            self._open_persistent_editors()
            
        except Exception as e:
            log_exception(e, f'Failed to load strategy data for {self.strategy_name}',
                         category='strategy_tab', action='load_strategy_data')
    
    def _setup_strategy_delegates(self):
        """Set up custom delegates with strategy_id for database updates."""
        try:
            # Enable editing on the model
            self.table_model.set_editable(True, True)
            
            # Set stint type combo delegate (column 0)
            self.stint_table.table.setItemDelegateForColumn(
                ColumnIndex.STINT_TYPE,
                StintTypeCombo(
                    self.stint_table.table,
                    update_doc=True,
                    strategy_id=str(self.strategy_id)
                )
            )
            
            # Set tire combo delegate (column 4)
            self.stint_table.table.setItemDelegateForColumn(
                ColumnIndex.TIRES_CHANGED,
                TireComboDelegate(
                    self.stint_table.table,
                    update_doc=True,
                    strategy_id=str(self.strategy_id)
                )
            )
            
            log('DEBUG', f'Strategy delegates configured for {self.strategy_name}',
                category='strategy_tab', action='setup_strategy_delegates')
            
        except Exception as e:
            log_exception(e, 'Failed to setup strategy delegates',
                         category='strategy_tab', action='setup_strategy_delegates')
    
    def _open_persistent_editors(self):
        """Open persistent editors for editable columns in all rows."""
        try:
            row_count = self.table_model.rowCount()
            
            for row in range(row_count):
                # Open editor for stint type column (only if cell has content)
                stint_type_index = self.table_model.index(row, ColumnIndex.STINT_TYPE)
                cell_text = str(stint_type_index.data())
                
                if cell_text:  # Non-empty cells get persistent editors
                    self.stint_table.table.openPersistentEditor(stint_type_index)
                else:  # Empty cells (pending stints) don't get editors
                    self.stint_table.table.closePersistentEditor(stint_type_index)
                
                # Always open editor for tire changes column
                tires_index = self.table_model.index(row, ColumnIndex.TIRES_CHANGED)
                self.stint_table.table.openPersistentEditor(tires_index)
            
            # Resize columns to fit editor content
            self.stint_table.table.resizeColumnsToContents()
            
            log('DEBUG', f'Opened persistent editors for {row_count} rows',
                category='strategy_tab', action='open_persistent_editors')
            
        except Exception as e:
            log_exception(e, 'Failed to open persistent editors',
                         category='strategy_tab', action='open_persistent_editors')
