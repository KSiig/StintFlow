from __future__ import annotations

from datetime import timedelta

from core.database import update_strategy
from core.errors import log, log_exception
from ui.models.mongo_docs_to_rows import mongo_docs_to_rows
from ui.models.stint_helpers import sanitize_stints


def _on_exclude_clicked(self, row: int) -> None:
    """Persist exclude toggle changes and refresh the view."""
    try:
        row_data, tire_data, _ = self.table_model.get_all_data()
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
                log(
                    'WARNING',
                    'Failed to realign rows after exclude toggle',
                    category='strategy_tab',
                    action='exclude_click',
                )

        rows = mongo_docs_to_rows(model_data['rows'])
        tires = model_data['tires']
        self.table_model.update_data(
            data=rows,
            tires=tires,
            mean_stint_time=timedelta(seconds=mean_sec),
        )
        try:
            self.table_model._recalculate_tires_left()
            self.table_model.update_mean(update_pending=False)
        except Exception:
            pass

        update_strategy(strategy=self.strategy)
        self.stint_table.refresh_table(skip_model_update=True)
        try:
            self._setup_strategy_delegates()
            self._open_persistent_editors()
        except Exception:
            pass
    except Exception as e:
        log_exception(
            e,
            'Failed to handle exclude click',
            category='strategy_tab',
            action='exclude_click',
        )
