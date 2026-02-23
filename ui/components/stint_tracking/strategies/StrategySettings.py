"""
StrategySettings component for the strategy tab placeholder.

Displays a placeholder for future strategy settings UI.
"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame, QCheckBox
from PyQt6.QtCore import Qt, pyqtSignal

from core.utilities import resource_path
from core.errors import log
from core.database import update_strategy
from ui.components.common import LabeledInputRow, SectionHeader, ConfigButton
from ui.models.mongo_docs_to_rows import mongo_docs_to_rows
from ui.models.table_processors import generate_pending_stints
from ui.models.table_constants import ColumnIndex
from ..config import ConfigLabels
from ui.components.stint_tracking.config.config_constants import ConfigLayout
from ui.models import ModelContainer
from ui.models.stint_helpers import get_default_tire_dict, sanitize_stints
from datetime import timedelta, datetime

class StrategySettings(QWidget):
    """
    Placeholder widget for strategy settings/info box.

    Fields include:
      * mean_stint_time - editable time string
      * lock_completed_stints - checkbox that prevents editing of already
        completed stints when enabled

    The lock checkbox is read-only until the user clicks the "edit"
    button; it becomes enabled during edit mode and is disabled again when
    the settings are saved.
    """

    strategy_updated = pyqtSignal(dict)  # Emitted when strategy is updated

    def __init__(self, parent=None, models: ModelContainer=None, strategy=None):
        super().__init__(parent)

        self.selection_model = models.selection_model
        self.table_model = models.table_model
        self.inputs = {}
        self.strategy = strategy

        self._setup_styles()
        self._setup_ui()
        self.table_model.dataChanged.connect(lambda: self._data_changed()) 
    
    def _data_changed(self):
        mean_stint_time = self.table_model._mean_stint_time if self.table_model else None
        self._set_inputs(mean_stint_time=mean_stint_time)
    
    def _setup_styles(self) -> None:
        """Load and apply strategy settings stylesheet."""
        try:
            with open(resource_path('resources/styles/strategy_settings.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except FileNotFoundError:
            log('WARNING', 'Strategy settings stylesheet not found', 
                category='strategy_settings', action='load_stylesheet')

    def _setup_ui(self):
        """Set up the UI layout for strategy settings."""

        layout = QVBoxLayout(self)
        frame = QFrame(self)
        frame.setObjectName("StrategySettingsFrame")
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setFrameShadow(QFrame.Shadow.Raised)

        frame_layout = QVBoxLayout(frame)
        header = SectionHeader(
            title="Strategy Settings",
            icon_path="resources/icons/race_config/settings.svg",
            icon_color="#05fd7e",
            icon_size=20,
            spacing=8
        )
        header.setObjectName("StrategySettingsHeader")
        frame_layout.setContentsMargins(4, 8, 4, 8)
        frame_layout.setSpacing(12)

        frame_layout.addWidget(header)
        mean_stint_time = self.table_model._mean_stint_time if self.table_model else None

        # Buttons (Edit / Save)
        btn_row = QVBoxLayout()
        self.edit_btn = ConfigButton(ConfigLabels.BTN_EDIT, icon_path="resources/icons/race_config/square-pen.svg", width_type="half")
        self.save_btn = ConfigButton(ConfigLabels.BTN_SAVE, icon_path="resources/icons/race_config/square-pen.svg", width_type="half")
        self.save_btn.hide()
        self.edit_btn.clicked.connect(self._toggle_edit)
        self.save_btn.clicked.connect(self._on_save_clicked)


        self._create_labeled_input_rows(frame_layout)
        self._set_inputs(mean_stint_time=mean_stint_time)

        frame_layout.addStretch()

        btn_row.addWidget(self.edit_btn)
        btn_row.addWidget(self.save_btn)
        frame_layout.addLayout(btn_row)

        frame.setLayout(frame_layout)

        layout.addWidget(frame)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)

    def _create_labeled_input_rows(self, layout: QVBoxLayout):
        """Create labeled input rows for strategy settings."""
                # Create and store input field references
        for field_id, title in [
            ("mean_stint_time", "Mean Stint Time"),
        ]:
            card = LabeledInputRow(title=title, input_height=ConfigLayout.INPUT_HEIGHT)
            self.inputs[field_id] = card.get_input_field()
            layout.addWidget(card)

        # additional options below the line of inputs
        # checkbox for locking completed stints
        lock_cb = QCheckBox(text="Lock completed stints")
        lock_cb.setEnabled(False)  # initially non-editable until user clicks edit
        self.inputs["lock_completed_stints"] = lock_cb
        layout.addWidget(lock_cb)

    def _toggle_edit(self):
        """Toggle edit mode for the input rows."""
        # If save button visible, switch to view mode
        edit_mode = self.save_btn.isVisible()
        if edit_mode:
            self.save_btn.hide()
            self.edit_btn.show()
        else:
            self.edit_btn.hide()
            self.save_btn.show()

        # iterate through inputs and adjust depending on type
        for widget in self.inputs.values():
            # QLineEdit-style widgets use readOnly property and style tweaks
            try:
                if hasattr(widget, 'setReadOnly'):
                    widget.setReadOnly(edit_mode)
                    widget.setProperty('editable', not edit_mode)
                    widget.style().unpolish(widget)
                    widget.style().polish(widget)
                    continue
            except Exception:
                pass

            # QCheckBox (or other) use enabled state
            try:
                widget.setEnabled(not edit_mode)
            except Exception:
                pass

    def _on_save_clicked(self):
        """Save handler for mean_stint_time and update related rows."""
        try:
            # 1. Retrieve and convert mean_stint_time from input
            input_widget = self.inputs.get("mean_stint_time")
            if input_widget is None:
                log('ERROR', 'mean_stint_time input widget missing', category='strategy_settings', action='save_clicked')
                return
            mean_stint_time_str = input_widget.text().strip()
            # Convert HH:MM:SS to seconds (int)
            try:
                h, m, s = map(int, mean_stint_time_str.split(":"))
                mean_stint_time_sec = h * 3600 + m * 60 + s
            except Exception as e:
                log('ERROR', f'Failed to parse mean_stint_time_str: {mean_stint_time_str}', category='strategy_settings', action='parse_time')
                return
            if mean_stint_time_sec is None:
                return

            # pull fresh data from the live table model rather than
            # trusting the stored strategy copy. this captures any edits
            # the user made after the strategy was opened.
            row_data, tire_data, _ = self.table_model.get_all_data()
            sanitized = sanitize_stints(row_data, tire_data)

            # overwrite strategy document with sanitized values from the
            # table; we'll then run _realign_rows on these entries.
            model_data = self.strategy.setdefault('model_data', {})
            model_data['rows'] = sanitized.get('rows', [])
            model_data['tires'] = sanitized.get('tires', [])

            # adjust existing pending rows in place (does not add/remove)
            self._realign_rows(mean_stint_time_sec)

            # refresh table model so the view reflects any pit-time shifts
            from datetime import timedelta as _td
            rows = model_data['rows']
            tires = model_data['tires']
            table_rows = mongo_docs_to_rows(rows)
            self.table_model.update_data(data=table_rows, tires=tires, mean_stint_time=_td(seconds=mean_stint_time_sec))
            self.table_model._recalculate_tires_left()
            self.table_model.update_mean(update_pending=False)

            # persist new mean and entire strategy document
            self.strategy['mean_stint_time_seconds'] = mean_stint_time_sec
            # also store checkbox state if present
            lock_widget = self.inputs.get("lock_completed_stints")
            if lock_widget is not None:
                self.strategy['lock_completed_stints'] = bool(lock_widget.isChecked())

            update_strategy(strategy=self.strategy)

            self.strategy_updated.emit(self.strategy)  # Emit updated strategy data for other components to react

            log('INFO', f'StrategySettings saved',
                category='strategy_settings', action='save_clicked')
        except Exception as e:
            log('ERROR', f'Exception in _on_save_clicked: {e}', category='strategy_settings', action='save_clicked')
        # Revert to view mode after pressing save
        self._toggle_edit()

    def _realign_rows(self, new_mean_sec):
        """Adjust pending rows to align with new mean stint time.

        This method directly mutates ``self.strategy['model_data']['rows']``.
        It performs two tasks:

        1.  Update every row document to carry the new
            ``stint_time_seconds`` value.
        2.  Recalculate the ``pit_end_time`` values for *pending* rows
            (those with ``status`` == False) so that the interval between
            successive pit times matches ``new_mean_sec``.  Pending rows are
            regenerated from the last completed entry; this also ensures the
            list grows or shrinks as necessary when the mean changes.

        The algorithm is essentially a stripped-down version of
        :func:`ui.models.table_processors.stint_processor.generate_pending_stints`
        adapted for our dictionary-based strategy representation.
        """
        model_data = self.strategy.setdefault('model_data', {})
        rows: list[dict] = model_data.setdefault('rows', [])

        # nothing to do if there are no rows at all
        if not rows:
            return

        # identify end of completed stints
        completed_count = 0
        for i, row in enumerate(rows):
            if row.get('status'):
                completed_count = i + 1
            else:
                break

        # if there are no completed stints we cannot compute a starting
        # pit time for pending calculations, so we're done after updating
        # the durations above.
        if completed_count == 0:
            return

        # Update all pending rows with new mean value
        for i in range(completed_count, len(rows)):
            rows[i]['stint_time_seconds'] = new_mean_sec

        # compute the starting point for pit time adjustments
        last_completed = rows[completed_count - 1]
        current_pit = last_completed.get('pit_end_time', '00:00:00')

        # we only need the subtraction helper for pit times and the
        # midnight-detection predicate
        from datetime import timedelta
        from ui.models.table_processors.stint_processor import (
            _subtract_time_from_pit_time,
            is_last_stint,
        )

        mean_td = timedelta(seconds=new_mean_sec)

        # iterate over existing pending rows and shift each pit time by the
        # new mean. we'll stop early if the sequence would cross midnight so
        # that we never generate times from the previous day. the durations
        # have already been updated above.
        keep_len = len(rows)
        for i in range(completed_count, len(rows)):
            # before subtracting, check whether the next subtraction would
            # cross into the previous day. if so we mark this row as the
            # midnight stump and drop everything after it.
            if is_last_stint(current_pit, mean_td):
                rows[i]['pit_end_time'] = "00:00:00"
                keep_len = i + 1
                break

            current_pit = _subtract_time_from_pit_time(current_pit, mean_td)
            rows[i]['pit_end_time'] = current_pit

        # truncate any entries that were beyond midnight; slices are safe
        # even if keep_len == len(rows)
        if keep_len < len(rows):
            rows[:] = rows[:keep_len]
            model_data['tires'] = model_data.get('tires', [])[:keep_len]

        # recalc current_pit based on trimmed list
        if len(rows) > completed_count:
            current_pit = rows[-1]['pit_end_time']
        else:
            current_pit = last_completed.get('pit_end_time', '00:00:00')

        # after realignment, it may be necessary to append or remove rows
        # depending on whether the timer has reached midnight. if the last
        # pit is still above 00:00:00 we'll add until we hit (or cross) it;
        # if the last pit landed exactly on midnight we are done.
        from ui.models.stint_helpers import get_default_tire_dict
        from ui.models.table_constants import FULL_TIRE_SET

        # alternating pattern: start with 0-change if an even number of
        # pending rows exist (including 0), otherwise start with 4.
        pending_count = len(rows) - completed_count
        next_change = 0 if pending_count % 2 == 0 else 4

        # compute tires_left starting value from last row (completed or
        # pending) so we can decrement when a full set change occurs.
        try:
            tires_left = int(rows[-1]['tires_left'])
        except Exception:
            tires_left = 0

        while True:
            # if current pit is already midnight we stop adding
            if current_pit == "00:00:00":
                break

            crossed = is_last_stint(current_pit, mean_td)
            next_pit = _subtract_time_from_pit_time(current_pit, mean_td)

            if crossed:
                # final crossing stint: show midnight with truncated duration
                pit_display = "00:00:00"
                from datetime import time as _time, date
                t_cur = datetime.strptime(current_pit, "%H:%M:%S").time()
                dt_cur = datetime.combine(date.today(), t_cur)
                dt_mid = datetime.combine(date.today(), _time(0, 0))
                duration_sec = int((dt_cur - dt_mid).total_seconds())
            else:
                pit_display = next_pit
                duration_sec = new_mean_sec

            # determine tires_left decrement
            if next_change == 4:
                tires_left -= FULL_TIRE_SET

            rows.append(
                {
                    "stint_type": "Single",
                    "name": "",
                    "status": False,
                    "pit_end_time": pit_display,
                    "tires_changed": next_change,
                    "tires_left": tires_left,
                    "stint_time_seconds": duration_sec,
                }
            )
            # append corresponding tire metadata
            model_data.setdefault('tires', []).append(
                get_default_tire_dict(next_change == 4)
            )

            if crossed:
                break

            current_pit = next_pit
            next_change = 4 if next_change == 0 else 0
        

    def _set_inputs(self, mean_stint_time=None):
        """Set the values of the input fields."""
        if mean_stint_time is not None:
            mean_stint_time_str = self._format_stint_time(mean_stint_time)

            # Ensure the input field exists before setting text
            widget = self.inputs.get("mean_stint_time")
            if widget is not None:
                widget.setText(mean_stint_time_str)

        # if strategy has lock setting, update checkbox
        # Only update the lock checkbox when not in edit mode.  The
        # table_model can emit dataChanged frequently, and we don't want to
        # stomp user edits while they are typing.  If we're currently in
        # edit mode the save button will be visible, so skip resetting.
        if not self.save_btn.isVisible():
            lock_widget = self.inputs.get("lock_completed_stints")
            if lock_widget is not None:
                # default unchecked if no strategy or field not set
                checked = False
                if self.strategy is not None:
                    checked = bool(self.strategy.get('lock_completed_stints', False))
                lock_widget.setChecked(checked)

    def _format_stint_time(self, stint_time) -> str:
        """Return a HH:MM:SS string for the provided stint_time.

        Accepts datetime.timedelta, string (possibly containing microseconds),
        or numeric seconds. Falls back to str(value) on unexpected input.
        """
        # Handle timedelta objects by stripping microseconds
        if isinstance(stint_time, timedelta):
            return str(stint_time).split('.', 1)[0]

        # Handle string representations like '0:27:07.800000'
        if isinstance(stint_time, str):
            return stint_time.split('.', 1)[0]

        # Try to interpret as seconds (numeric) and format H:MM:SS
        try:
            total_seconds = int(float(stint_time))
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        except Exception:
            return str(stint_time)