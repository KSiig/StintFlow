from __future__ import annotations

from datetime import timedelta

from core.database import update_strategy
from core.errors import log_exception
from ui.models.mongo_docs_to_rows import mongo_docs_to_rows
from ui.models.stint_helpers import sanitize_stints


def _on_delete_clicked(self, row: int, strategy_id: str | None = None) -> None:
    """Delete a stint row from the strategy and persist changes."""
    try:
        row_data, tire_data, _ = self.table_model.get_all_data()

        if 0 <= row < len(row_data):
            del row_data[row]
        if 0 <= row < len(tire_data):
            del tire_data[row]

        sanitized = sanitize_stints(row_data, tire_data)
        model_data = self.strategy.setdefault('model_data', {})
        model_data['rows'] = sanitized.get('rows', [])
        model_data['tires'] = sanitized.get('tires', [])
        self.strategy['model_data'] = model_data

        table_rows = mongo_docs_to_rows(model_data['rows'])
        self.table_model.update_data(data=table_rows, tires=model_data['tires'])
        try:
            self.table_model._recalculate_tires_left()
            self.table_model.update_mean(update_pending=False)
        except Exception:
            pass

        mean_sec = int(self.table_model._mean_stint_time.total_seconds())
        self.strategy['mean_stint_time_seconds'] = mean_sec
        update_strategy(strategy=self.strategy)

        if hasattr(self, 'strategy_settings'):
            try:
                self.strategy_settings._realign_rows(mean_sec)
            except Exception:
                from core.errors import log

                log(
                    'WARNING',
                    'Failed to realign rows after delete',
                    category='strategy_tab',
                    action='delete_stint',
                )

        rows = mongo_docs_to_rows(self.strategy['model_data'].get('rows', []))
        tires = self.strategy['model_data'].get('tires', [])
        self.table_model.update_data(
            data=rows,
            tires=tires,
            mean_stint_time=timedelta(seconds=mean_sec),
        )
        self.table_model._recalculate_tires_left()
        self.table_model.update_mean(update_pending=False)

        self.stint_table.refresh_table(skip_model_update=True)
    except Exception as e:
        log_exception(
            e,
            'Failed to delete strategy stint',
            category='strategy_tab',
            action='delete_stint',
        )
