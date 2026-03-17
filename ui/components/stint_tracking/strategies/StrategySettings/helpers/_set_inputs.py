from __future__ import annotations

from core.utilities import format_stint_time


def _set_inputs(self) -> None:
    """Populate input widgets from current model and strategy state."""
    if self._has_unsaved_input_changes:
        return

    input_state = {
        'name': self.strategy.get('name', '') if self.strategy else '',
        'mean_stint_time': '',
        'lock_completed_stints': bool(self.strategy.get('lock_completed_stints', False)) if self.strategy else False,
    }

    mean_stint_time = self.table_model._mean_stint_time if self.table_model else None
    if mean_stint_time is not None:
        input_state['mean_stint_time'] = format_stint_time(mean_stint_time)

    self._apply_input_state(input_state, persist_as_committed=True)
