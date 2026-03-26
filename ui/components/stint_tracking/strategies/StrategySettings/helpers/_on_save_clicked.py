from __future__ import annotations

from datetime import timedelta

from core.database import update_strategy
from core.errors import log, log_exception
from ui.models.mongo_docs_to_rows import mongo_docs_to_rows
from ui.models.stint_helpers import sanitize_stints


def _on_save_clicked(self) -> None:
    """Persist strategy updates and refresh the model state."""
    try:
        input_widget = self.inputs.get("mean_stint_time")
        if input_widget is None:
            log(
                'ERROR',
                'mean_stint_time input widget missing',
                category='strategy_settings',
                action='save_clicked',
            )
            return

        mean_stint_time_str = input_widget.text().strip()
        stint_name_widget = self.inputs.get("name")
        if stint_name_widget is not None and self.strategy is not None:
            self.strategy['name'] = stint_name_widget.text().strip()

        try:
            h, m, s = map(int, mean_stint_time_str.split(":"))
            mean_stint_time_sec = h * 3600 + m * 60 + s
        except Exception:
            log(
                'ERROR',
                f'Failed to parse mean_stint_time_str: {mean_stint_time_str}',
                category='strategy_settings',
                action='parse_time',
            )
            return

        if mean_stint_time_sec is None:
            return

        row_data, tire_data, _ = self.table_model.get_all_data()
        sanitized = sanitize_stints(row_data, tire_data)

        model_data = self.strategy.setdefault('model_data', {})
        model_data['rows'] = sanitized.get('rows', [])
        model_data['tires'] = sanitized.get('tires', [])

        self._realign_rows(mean_stint_time_sec)

        rows = model_data['rows']
        tires = model_data['tires']
        table_rows = mongo_docs_to_rows(rows)
        self.table_model.update_data(
            data=table_rows,
            tires=tires,
            mean_stint_time=timedelta(seconds=mean_stint_time_sec),
        )
        self.table_model._recalculate_tires_left()
        self.table_model.update_mean(update_pending=False)

        self.strategy['mean_stint_time_seconds'] = mean_stint_time_sec
        lock_widget = self.inputs.get("lock_completed_stints")
        if lock_widget is not None:
            self.strategy['lock_completed_stints'] = bool(lock_widget.isChecked())

        update_strategy(strategy=self.strategy)
        self.strategy_updated.emit(self.strategy)
        self._committed_input_state = self._capture_input_state()
        self._has_unsaved_input_changes = False
        self.save_btn.hide()
        self.cancel_btn.hide()

        log(
            'INFO',
            'Strategy settings saved',
            category='strategy_settings',
            action='save_clicked',
        )
    except Exception as e:
        log('ERROR', f'Exception in _on_save_clicked: {e}', category='strategy_settings', action='save_clicked')
        log_exception(
            e,
            'Failed to save strategy settings',
            category='strategy_settings',
            action='save_clicked',
        )

