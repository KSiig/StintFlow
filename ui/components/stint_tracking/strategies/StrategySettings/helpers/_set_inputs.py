from __future__ import annotations

from core.utilities import format_stint_time


def _set_inputs(self) -> None:
    """Populate input widgets from current model and strategy state."""
    mean_stint_time = self.table_model._mean_stint_time if self.table_model else None
    if mean_stint_time is not None:
        mean_stint_time_str = format_stint_time(mean_stint_time)
        widget = self.inputs.get("mean_stint_time")
        if widget is not None:
            widget.setText(mean_stint_time_str)

    if self.strategy is not None:
        name_widget = self.inputs.get("name")
        if name_widget is not None:
            name_widget.setText(self.strategy.get('name', ''))

    if not self.save_btn.isVisible():
        lock_widget = self.inputs.get("lock_completed_stints")
        if lock_widget is not None:
            checked = bool(self.strategy.get('lock_completed_stints', False)) if self.strategy else False
            lock_widget.setChecked(checked)
