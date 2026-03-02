from __future__ import annotations

from datetime import timedelta

from core.errors import log, log_exception
from ui.models.mongo_docs_to_rows import mongo_docs_to_rows


def _load_strategy_data(self) -> None:
    """Load strategy stints into the table model and configure delegates."""
    try:
        model_data = self.strategy.get('model_data', {})
        stints = model_data.get('rows', [])
        tires = model_data.get('tires', [])
        mean_stint_time_seconds = self.strategy.get('mean_stint_time_seconds', 0)

        if not stints:
            log(
                'INFO',
                f'No stints in strategy {self.strategy_name}',
                category='strategy_tab',
                action='load_strategy_data',
            )
            return

        rows = mongo_docs_to_rows(stints)
        self.table_model.update_data(
            data=rows,
            tires=tires,
            mean_stint_time=timedelta(seconds=mean_stint_time_seconds),
        )

        self._setup_strategy_delegates()
        self.table_model._recalculate_tires_left()

        log(
            'DEBUG',
            f'Loaded {len(rows)} stints for strategy {self.strategy_name}',
            category='strategy_tab',
            action='load_strategy_data',
        )

        self._open_persistent_editors()
        self.stint_table._set_column_widths()
    except Exception as e:
        log_exception(
            e,
            f'Failed to load strategy data for {self.strategy_name}',
            category='strategy_tab',
            action='load_strategy_data',
        )
