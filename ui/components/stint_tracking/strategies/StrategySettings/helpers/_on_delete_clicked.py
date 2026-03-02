from __future__ import annotations

from PyQt6.QtWidgets import QMessageBox

from core.database import delete_strategy
from core.errors import log, log_exception


def _on_delete_clicked(self) -> None:
    """Ask for confirmation and delete the current strategy."""
    if not self.strategy or not self.strategy.get('_id'):
        log(
            'WARNING',
            'Delete requested but no strategy id available',
            category='strategy_settings',
            action='delete_clicked',
        )
        return

    resp = QMessageBox.question(
        self,
        'Delete Strategy',
        'Are you sure you want to delete this strategy? This action cannot be undone.',
        QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
    )
    if resp != QMessageBox.StandardButton.Yes:
        return

    try:
        sid = str(self.strategy.get('_id'))
        success = delete_strategy(sid)
        if success:
            log(
                'INFO',
                f'Strategy {sid} deleted',
                category='strategy_settings',
                action='delete_clicked',
            )
            self.strategy_deleted.emit(sid)
        else:
            log(
                'WARNING',
                f'Failed to delete strategy {sid}',
                category='strategy_settings',
                action='delete_clicked',
            )
    except Exception as e:
        log_exception(
            e,
            'Exception deleting strategy',
            category='strategy_settings',
            action='delete_clicked',
        )
