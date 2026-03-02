from __future__ import annotations

from core.errors import log, log_exception
from ui.models.table_constants import ColumnIndex
from ....delegates import ActionsDelegate, StintTypeCombo, TireComboDelegate


def _setup_strategy_delegates(self) -> None:
    """Configure delegates for strategy editing with locking support."""
    try:
        self.table_model.set_editable(True, True)

        lock_enabled = bool(self.strategy.get('lock_completed_stints', False))
        self._lock_completed = lock_enabled

        stint_delegate = StintTypeCombo(
            self.stint_table.table,
            update_doc=True,
            strategy_id=str(self.strategy_id),
        )
        stint_delegate.lock_completed = lock_enabled
        self.stint_table.table.setItemDelegateForColumn(ColumnIndex.STINT_TYPE, stint_delegate)

        tire_delegate = TireComboDelegate(
            self.stint_table.table,
            update_doc=True,
            strategy_id=str(self.strategy_id),
        )
        tire_delegate.lock_completed = lock_enabled
        self.stint_table.table.setItemDelegateForColumn(ColumnIndex.TIRES_CHANGED, tire_delegate)

        self.actions_delegate = ActionsDelegate(
            self.stint_table.table,
            update_doc=True,
            strategy_id=str(self.strategy_id),
        )
        self.actions_delegate.deleteClicked.connect(self._on_delete_clicked)
        self.actions_delegate.excludeClicked.connect(self._on_exclude_clicked)

        self.stint_table.table.setItemDelegateForColumn(ColumnIndex.ACTIONS, self.actions_delegate)
        self.stint_table.actions_delegate = self.actions_delegate
        self.stint_table._set_column_widths()

        log(
            'DEBUG',
            f'Strategy delegates configured for {self.strategy_name}',
            category='strategy_tab',
            action='setup_strategy_delegates',
        )
    except Exception as e:
        log_exception(
            e,
            'Failed to setup strategy delegates',
            category='strategy_tab',
            action='setup_strategy_delegates',
        )
