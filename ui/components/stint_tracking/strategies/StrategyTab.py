"""
Strategy display tab.

Shows an existing strategy with editable stint table.
"""

from datetime import timedelta
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QSizePolicy
from PyQt6.QtCore import pyqtSignal
from core.errors import log, log_exception
from core.utilities import resource_path
from core.database import update_strategy
from ui.models import TableModel, SelectionModel, ModelContainer
from ui.models.table_constants import ColumnIndex
from ui.models.mongo_docs_to_rows import mongo_docs_to_rows
from ui.models.stint_helpers import sanitize_stints
from ..widgets import StintTable
from ..delegates import TireComboDelegate, StintTypeCombo, ActionsDelegate
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
        
        # Clone table model for independent state and mark it as a
        # strategy-specific copy so that mean updates behave differently.
        self.table_model = table_model.clone()
        self.table_model._is_strategy = True
        
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
            layout.setSpacing(12)

            models = ModelContainer(
                selection_model=self.selection_model,
                table_model=self.table_model
            )

            # StrategySettings component for top half
            strategy_settings = StrategySettings(self, models, self.strategy)
            # keep a reference for later operations (e.g. after deletions)
            self.strategy_settings = strategy_settings
            strategy_settings.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            # when the settings change we want to update both the table and
            # potentially the tab label if the strategy name was edited
            strategy_settings.strategy_updated.connect(self._strategy_updated)
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

    # signal emitted when this tab's strategy name changes; the parent
    # view uses it to keep the tab bar text in sync.
    name_changed = pyqtSignal(str)

    def _strategy_updated(self, updated_strategy: dict):
        """Handle updates to the strategy from StrategySettings.

        This is called whenever the user saves changes in the settings pane.
        In addition to reloading table data, if the name field was modified we
        update the cached ``self.strategy_name`` and emit ``name_changed`` so
        that any container (e.g. ``StrategiesView``) can adjust its tab label
        without rebuilding all the tabs.
        """
        self.strategy = updated_strategy

        # notify parent if name has changed
        # new_name = self.strategy.get('name')
        # if new_name and new_name != old_name:
        #     self.strategy_name = new_name
        self.name_changed.emit(self.strategy.get('name', 'Unnamed Strategy'))

        self._load_strategy_data()  # Reload table with updated strategy data
        self.table_model._recalculate_tires_left()
    
    def _load_strategy_data(self):
        """Load strategy stints from MongoDB and populate table."""
        try:
            # Get model_data from strategy document
            model_data = self.strategy.get('model_data', {})
            stints = model_data.get('rows', [])
            tires = model_data.get('tires', [])
            mean_stint_time_seconds = self.strategy.get('mean_stint_time_seconds', 0)
            
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
            self.table_model._recalculate_tires_left()
            
            log('DEBUG', f'Loaded {len(rows)} stints for strategy {self.strategy_name}',
                category='strategy_tab', action='load_strategy_data')
            
            # Open persistent editors for editable columns
            self._open_persistent_editors()

            # Re-apply column widths now that the table is fully populated
            # and delegates are in place. In strategy tabs the earlier call
            # in _setup_strategy_delegates() can occur before the table is
            # shown, so we repeat it here to avoid incorrect header length.
            self.stint_table._set_column_widths()

        except Exception as e:
            log_exception(e, f'Failed to load strategy data for {self.strategy_name}',
                         category='strategy_tab', action='load_strategy_data')

    # ------------------------------------------------------------------
    # Delete handler
    # ------------------------------------------------------------------

    def _on_delete_clicked(self, row: int, strategy_id: str | None = None) -> None:
        """Handle user request to delete a stint from the strategy.

        ``strategy_id`` parameter is accepted for signal compatibility but is
        ignored since the tab already knows its own strategy ID.

        Removes the row from both the strategy document stored in MongoDB and
        the in‑memory table model.  The index is deleted from
        ``model_data.rows`` and ``model_data.tires``; the mean stint time is
        recalculated and persisted as well.
        """
        try:
            # start from the current table model state; this ensures we
            # honour any user edits that haven't yet been written to the
            # strategy document.
            row_data, tire_data, _ = self.table_model.get_all_data()

            # remove the specified row from the display lists
            if 0 <= row < len(row_data):
                del row_data[row]
            if 0 <= row < len(tire_data):
                del tire_data[row]

            # sanitize into mongo‑compatible documents and store in strategy
            from ui.models.stint_helpers import sanitize_stints
            sanitized = sanitize_stints(row_data, tire_data)
            model_data = self.strategy.setdefault('model_data', {})
            model_data['rows'] = sanitized.get('rows', [])
            model_data['tires'] = sanitized.get('tires', [])
            self.strategy['model_data'] = model_data

            # push change back into table model as well
            table_rows = mongo_docs_to_rows(model_data['rows'])
            self.table_model.update_data(data=table_rows, tires=model_data['tires'])
            try:
                self.table_model._recalculate_tires_left()
                self.table_model.update_mean(update_pending=False)  # Recalc mean without regenerating pending stints
            except Exception:
                pass

            # recalc mean and persist strategy
            mean_sec = int(self.table_model._mean_stint_time.total_seconds())
            self.strategy['mean_stint_time_seconds'] = mean_sec
            update_strategy(strategy=self.strategy)

            # realign any pending stints in the strategy just like Save does
            if hasattr(self, 'strategy_settings'):
                try:
                    self.strategy_settings._realign_rows(mean_sec)
                except Exception:
                    # not critical; log and continue
                    log('WARNING', 'Failed to realign rows after delete',
                        category='strategy_tab', action='delete_stint')

            # refresh the table model from updated document so that
            # pending pit times reflect the adjusted mean
            rows = mongo_docs_to_rows(self.strategy['model_data'].get('rows', []))
            tires = self.strategy['model_data'].get('tires', [])
            self.table_model.update_data(data=rows, tires=tires, mean_stint_time=timedelta(seconds=mean_sec))
            self.table_model._recalculate_tires_left()
            self.table_model.update_mean(update_pending=False)

            # Update view without touching the underlying data (already
            # applied above).  This will recalc placeholder/column widths.
            self.stint_table.refresh_table(skip_model_update=True)
        except Exception as e:
            log_exception(e, 'Failed to delete strategy stint',
                         category='strategy_tab', action='delete_stint')
    
    def _on_exclude_clicked(self, row: int) -> None:
        """Handle exclude/include toggle from the actions delegate.

        The delegate has already flipped the excluded flag and recalculated
        the model mean, but the strategy document and any pending stints need
        to be updated to follow suit.  This mirrors the behaviour performed
        when the user presses Save in the settings panel.
        """
        try:
            # base everything on the latest model data rather than the
            # stored document
            row_data, tire_data, _ = self.table_model.get_all_data()
            from ui.models.stint_helpers import sanitize_stints
            sanitized = sanitize_stints(row_data, tire_data)

            model_data = self.strategy.setdefault('model_data', {})
            model_data['rows'] = sanitized.get('rows', [])
            model_data['tires'] = sanitized.get('tires', [])

            mean_sec = int(self.table_model._mean_stint_time.total_seconds())
            self.strategy['mean_stint_time_seconds'] = mean_sec

            if hasattr(self, 'strategy_settings'):
                try:
                    self.strategy_settings._realign_rows(mean_sec)
                except Exception:
                    log('WARNING', 'Failed to realign rows after exclude toggle',
                        category='strategy_tab', action='exclude_click')

            # refresh the table model based on the possibly re-aligned rows
            rows = mongo_docs_to_rows(model_data['rows'])
            tires = model_data['tires']
            self.table_model.update_data(data=rows, tires=tires, mean_stint_time=timedelta(seconds=mean_sec))
            try:
                self.table_model._recalculate_tires_left()
                self.table_model.update_mean(update_pending=False)
            except Exception:
                # non-critical for strategy view, can fail if no event/session
                pass

            update_strategy(strategy=self.strategy)
            self.stint_table.refresh_table(skip_model_update=True)
            # keep editors and delegates alive after the refresh
            try:
                self._setup_strategy_delegates()
                self._open_persistent_editors()
            except Exception:
                pass
        except Exception as e:
            log_exception(e, 'Failed to handle exclude click',
                         category='strategy_tab', action='exclude_click')
    
    def _setup_strategy_delegates(self):
        """Set up custom delegates with strategy_id for database updates."""
        try:
            # Enable editing on the model
            self.table_model.set_editable(True, True)

            # determine whether completed rows should be locked
            lock_enabled = bool(self.strategy.get('lock_completed_stints', False))
            self._lock_completed = lock_enabled
            
            # Set stint type combo delegate (column 0)
            stint_delegate = StintTypeCombo(
                self.stint_table.table,
                update_doc=True,
                strategy_id=str(self.strategy_id)
            )
            stint_delegate.lock_completed = lock_enabled
            self.stint_table.table.setItemDelegateForColumn(
                ColumnIndex.STINT_TYPE,
                stint_delegate
            )
            
            # Set tire combo delegate (column 4)
            tire_delegate = TireComboDelegate(
                self.stint_table.table,
                update_doc=True,
                strategy_id=str(self.strategy_id)
            )
            tire_delegate.lock_completed = lock_enabled
            self.stint_table.table.setItemDelegateForColumn(
                ColumnIndex.TIRES_CHANGED,
                tire_delegate
            )

            # Set actions delegate 
            self.actions_delegate = ActionsDelegate(
                    self.stint_table.table,
                    update_doc=True,
                    strategy_id=str(self.strategy_id)
                )
            # wire up action buttons to handlers that maintain both the database
            # and the in‑memory model state
            self.actions_delegate.deleteClicked.connect(self._on_delete_clicked)
            self.actions_delegate.excludeClicked.connect(self._on_exclude_clicked)

            # replace the delegate on the table and update parent reference
            self.stint_table.table.setItemDelegateForColumn(
                ColumnIndex.ACTIONS,
                self.actions_delegate
            )
            self.stint_table.actions_delegate = self.actions_delegate
            self.stint_table._set_column_widths()  # Update column widths to fit new delegate
            
            log('DEBUG', f'Strategy delegates configured for {self.strategy_name}',
                category='strategy_tab', action='setup_strategy_delegates')
            
        except Exception as e:
            log_exception(e, 'Failed to setup strategy delegates',
                         category='strategy_tab', action='setup_strategy_delegates')
    
    def _open_persistent_editors(self):
        """Open persistent editors for editable columns in all rows."""
        try:
            row_count = self.table_model.rowCount()
            lock_enabled = getattr(self, '_lock_completed', False)

            for row in range(row_count):
                # determine completed status of this row
                status_idx = self.table_model.index(row, ColumnIndex.STATUS)
                status_val = status_idx.data()
                is_completed = status_val is not None and "Completed" in str(status_val)

                # Stint type column
                stint_type_index = self.table_model.index(row, ColumnIndex.STINT_TYPE)
                cell_text = str(stint_type_index.data())

                if lock_enabled and is_completed:
                    # skip editors for locked completed rows
                    self.stint_table.table.closePersistentEditor(stint_type_index)
                else:
                    if cell_text:  # Non-empty cells get persistent editors
                        self.stint_table.table.openPersistentEditor(stint_type_index)
                    else:  # Empty cells (pending stints) don't get editors
                        self.stint_table.table.closePersistentEditor(stint_type_index)

                # Tire changes column
                tires_index = self.table_model.index(row, ColumnIndex.TIRES_CHANGED)
                if lock_enabled and is_completed:
                    self.stint_table.table.closePersistentEditor(tires_index)
                else:
                    self.stint_table.table.openPersistentEditor(tires_index)

            # Resize columns to fit editor content
            self.stint_table.table.resizeColumnsToContents()

            log('DEBUG', f'Opened persistent editors for {row_count} rows',
                category='strategy_tab', action='open_persistent_editors')

        except Exception as e:
            log_exception(e, 'Failed to open persistent editors',
                         category='strategy_tab', action='open_persistent_editors')
