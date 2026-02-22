"""
StrategySettings component for the strategy tab placeholder.

Displays a placeholder for future strategy settings UI.
"""

from PyQt6.QtWidgets import QWidget, QLabel, QVBoxLayout, QFrame
from PyQt6.QtCore import Qt, pyqtSignal

from core.utilities import resource_path
from core.errors import log
from core.database import update_strategy
from ui.components.common import LabeledInputRow, SectionHeader, ConfigButton
from ui.models.mongo_docs_to_rows import mongo_docs_to_rows
from ui.models.table_processors import generate_pending_stints
from ..config import ConfigLabels
from ui.components.stint_tracking.config.config_constants import ConfigLayout
from ui.models import ModelContainer
from ui.models.stint_helpers import get_default_tire_dict
from datetime import timedelta, datetime

class StrategySettings(QWidget):
    """
    Placeholder widget for strategy settings/info box.
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

    def _toggle_edit(self):
        """Toggle edit mode for the input rows."""
        # If save button visible, switch to view mode
        if self.save_btn.isVisible():
            self.save_btn.hide()
            self.edit_btn.show()
            for widget in self.inputs.values():
                try:
                    widget.setReadOnly(True)
                    widget.setProperty('editable', False)
                    widget.style().unpolish(widget)
                    widget.style().polish(widget)
                except Exception:
                    pass
        else:
            # Enter edit mode
            self.edit_btn.hide()
            self.save_btn.show()
            for widget in self.inputs.values():
                try:
                    widget.setReadOnly(False)
                    widget.setProperty('editable', True)
                    widget.style().unpolish(widget)
                    widget.style().polish(widget)
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

            # ensure we have model_data dict to work with
            model_data = self.strategy.setdefault('model_data', {})
            rows = model_data.get('rows', [])
            tires = model_data.get('tires', [])

            # adjust existing pending rows and add extras if needed
            self._realign_rows(mean_stint_time_sec)

            # refresh table model to reflect updated strategy
            from datetime import timedelta as _td
            table_rows = mongo_docs_to_rows(rows)
            self.table_model.update_data(data=table_rows, tires=tires, mean_stint_time=_td(seconds=mean_stint_time_sec))
            self.table_model._recalculate_tires_left()
            self.table_model.update_mean(update_pending=False)

            # persist new mean and entire strategy document
            self.strategy['mean_stint_time_seconds'] = mean_stint_time_sec
            update_strategy(strategy=self.strategy)

            self.strategy_updated.emit(self.strategy)  # Emit updated strategy data for other components to react

            log('INFO', f'StrategySettings saved',
                category='strategy_settings', action='save_clicked')
        except Exception as e:
            log('ERROR', f'Exception in _on_save_clicked: {e}', category='strategy_settings', action='save_clicked')
        # Revert to view mode after pressing save
        self._toggle_edit()

    def _get_new_pit_end_time(self, prev_pit_end_time_str: str, mean_stint_time_sec: int) -> str:
        """Calculate new pit end time by subtracting mean stint time from previous pit end time."""
        try:
            h, m, s = map(int, prev_pit_end_time_str.split(":"))
            prev_seconds = h * 3600 + m * 60 + s
            new_seconds = max(prev_seconds - mean_stint_time_sec, 0)
            new_h = new_seconds // 3600
            new_m = (new_seconds % 3600) // 60
            new_s = new_seconds % 60
            return f"{new_h:02d}:{new_m:02d}:{new_s:02d}"
        except Exception as e:
            log('ERROR', f'Failed to calculate new pit end time: {prev_pit_end_time_str}', category='strategy_settings', action='calculate_pit_end_time')
            return prev_pit_end_time_str  # Fallback to original if error occurs

    def _realign_rows(self, mean_stint_time_sec=None):
        """Adjust existing pending rows and generate any additional ones.

        Existing pending rows are slid backwards from the last completed pit
        time using the supplied mean.  Only rows that hit zero are deleted;
        tires_changed values are preserved.  After updating the current pending
        set we call ``_add_rows`` to append any further stints required by the
        new mean.
        """
        rows = self.strategy['model_data'].get('rows', [])
        tires = self.strategy['model_data'].get('tires', [])

        # walk through rows sequentially, updating pending entries
        prev_time = None
        for row in rows:
            if row.get('status'):
                prev_time = row.get('pit_end_time')
            else:
                # pending row, compute new pit_end_time and duration
                if prev_time is None:
                    prev_time = '00:00:00'
                new_time = self._get_new_pit_end_time(prev_time, mean_stint_time_sec)
                row['pit_end_time'] = new_time
                row['stint_time_seconds'] = mean_stint_time_sec
                prev_time = new_time

        # remove any pending rows whose time has dropped to zero, along with
        # their tire metadata.  We cannot simply trim the end, because a rapid
        # mean reduction may push *middle* stints to zero while later ones
        # remain positive.
        zero_indices = []
        for idx, row in enumerate(rows):
            if not row.get('status'):
                pit = row.get('pit_end_time', '00:00:00')
                h, m, s = map(int, pit.split(":"))
                if h == 0 and m == 0 and s == 0:
                    zero_indices.append(idx)
        # delete backwards so indices remain valid
        for idx in reversed(zero_indices):
            del rows[idx]
            if idx < len(tires):
                del tires[idx]

        # after pruning invalid entries, append any additional pending stints
        # required by the new mean
        self._add_rows(mean_stint_time_sec)

    def _add_rows(self, mean_stint_time_sec=None):
        """Generate pending rows following the last completed stint.

        The previous implementation alternated tire changes blindly, causing
        all regenerated pending rows to inherit the wrong ``tires_changed``
        value.  Here we inspect the last completed row and follow the same
        rule used by ``generate_pending_stints`` in the shared processor.
        Existing strategy stints are never overwritten; only genuinely new
        rows receive default values.
        """
        rows = self.strategy['model_data'].get('rows', [])
        tires = self.strategy['model_data'].get('tires', [])
        if not rows:
            return

        last_row = rows[-1]
        while True:
            # compute current pit time seconds
            pit = last_row.get('pit_end_time', '00:00:00')
            h, m, s = map(int, pit.split(":"))
            seconds = h * 3600 + m * 60 + s
            if seconds == 0:
                break

            # determine number of tires changed based on previous row
            last_tire_change = int(last_row.get('tires_changed', 0))
            from ui.models.table_constants import FULL_TIRE_SET, NO_TIRE_CHANGE
            pending_tires_changed = FULL_TIRE_SET if last_tire_change == NO_TIRE_CHANGE else NO_TIRE_CHANGE

            # construct new pending row preserving other fields
            new_row = last_row.copy()
            new_row['pit_end_time'] = self._get_new_pit_end_time(pit, mean_stint_time_sec)
            new_row['tires_changed'] = pending_tires_changed
            rows.append(new_row)
            last_row = new_row

            # add new tire metadata based on whether any tires changed
            # (bool) rather than the raw count.  This keeps the strategy
            # document consistent with other parts of the code.
            tires.append(get_default_tire_dict(tires_changed=bool(pending_tires_changed)))

    def _set_inputs(self, mean_stint_time=None):
        """Set the values of the input fields."""
        if mean_stint_time is not None:
            mean_stint_time_str = self._format_stint_time(mean_stint_time)

            # Ensure the input field exists before setting text
            widget = self.inputs.get("mean_stint_time")
            if widget is not None:
                widget.setText(mean_stint_time_str)

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