from __future__ import annotations

from core.errors import log


def _on_delete_clicked(self, row: int, strategy_id: str | None = None) -> None:
    """Handle delete clicks from the actions delegate."""
    model = self.table.model()
    if model is None:
        return

    if hasattr(model, 'delete_stint'):
        try:
            model.delete_stint(row, strategy_id)
        except Exception as e:
            log('ERROR', f'Error deleting row {row}: {e}', category='stint_table', action='handle_delete')
    self.refresh_table()
