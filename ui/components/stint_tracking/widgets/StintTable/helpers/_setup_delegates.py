from __future__ import annotations

from ....delegates import ActionsDelegate, DriverPillDelegate, StatusDelegate, TireComboDelegate
from ui.models.table_constants import ColumnIndex


def _setup_delegates(self) -> None:
    """Configure custom delegates for styled columns."""
    self.table.setItemDelegateForColumn(ColumnIndex.DRIVER, DriverPillDelegate(self.table))
    self.table.setItemDelegateForColumn(ColumnIndex.STATUS, StatusDelegate(self.table))
    self.table.setItemDelegateForColumn(ColumnIndex.TIRES_CHANGED, TireComboDelegate(self.table))
    self.actions_delegate = ActionsDelegate(self.table)
    self.actions_delegate.deleteClicked.connect(self._on_delete_clicked)
    self.table.setItemDelegateForColumn(ColumnIndex.ACTIONS, self.actions_delegate)
    self.actions_delegate.excludeClicked.connect(lambda idx: None)
