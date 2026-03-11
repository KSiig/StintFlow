from __future__ import annotations

from ....delegates import StintTypeCombo, TireComboDelegate
from ui.models.table_constants import ColumnIndex
from core.errors import log


def _setup_editors(self) -> None:
    """Enable editing mode with combo delegates."""
    if self.table.model() is None:
        log('WARNING', 'Cannot setup editors - no model available', category='stint_table', action='setup_editors')
        return

    self.table.model().set_editable(editable=True, partial=True)

    self.table.setItemDelegateForColumn(
        ColumnIndex.TIRES_CHANGED,
        TireComboDelegate(self.table, update_doc=True),
    )
    self.table.setItemDelegateForColumn(
        ColumnIndex.STINT_TYPE,
        StintTypeCombo(self.table, update_doc=True),
    )
