"""Configuration panel for stint tracking."""

from PyQt6.QtCore import QProcess, pyqtSignal
from PyQt6.QtWidgets import QWidget

from ui.components.common import PopUp
from ui.models import ModelContainer
from ui.utilities.load_style import load_style
from core.errors import log_exception

from .helpers import (
    _add_config_rows,
    _apply_form_state,
    _can_switch_views,
    _cancel_changes,
    _capture_form_state,
    _clone_event,
    _create_button_layout,
    _create_buttons,
    _create_session,
    _handle_agent_registration_conflict,
    _handle_output,
    _handle_process_error,
    _handle_process_finished,
    _handle_save_shortcut,
    _handle_stderr,
    _handle_stdout,
    _flash_taskbar,
    _refresh_labels,
    _reset_info_lbl,
    _revert_tracking_state,
    _save_config,
    _setup_ui,
    _shutdown_tracking,
    _show_info_lbl,
    _start_process,
    _toggle_edit,
    _toggle_track,
)


class ConfigOptions(QWidget):
    """Configuration options widget for stint tracking."""

    stint_created = pyqtSignal()
    tracker_started = pyqtSignal()
    tracker_stopped = pyqtSignal()

    _setup_ui = _setup_ui
    _create_buttons = _create_buttons
    _add_config_rows = _add_config_rows
    _apply_form_state = _apply_form_state
    _can_switch_views = _can_switch_views
    _cancel_changes = _cancel_changes
    _capture_form_state = _capture_form_state
    _create_button_layout = _create_button_layout
    _handle_save_shortcut = _handle_save_shortcut
    _refresh_labels = _refresh_labels
    _flash_taskbar = _flash_taskbar
    _toggle_edit = _toggle_edit
    _save_config = _save_config
    _clone_event = _clone_event
    _create_session = _create_session
    _toggle_track = _toggle_track
    _start_process = _start_process
    _handle_stderr = _handle_stderr
    _handle_stdout = _handle_stdout
    _handle_output = _handle_output
    _show_info_lbl = _show_info_lbl
    _reset_info_lbl = _reset_info_lbl
    _handle_agent_registration_conflict = _handle_agent_registration_conflict
    _handle_process_error = _handle_process_error
    _handle_process_finished = _handle_process_finished
    _revert_tracking_state = _revert_tracking_state
    _shutdown_tracking = _shutdown_tracking

    def __init__(self, models: ModelContainer):
        super().__init__()

        self.selection_model = models.selection_model
        self.table_model = models.table_model
        self.event = None
        self.session = None
        self.team = None
        self.drivers = []
        self.inputs = {}
        self.driver_inputs = []
        self.p: QProcess | None = None
        self._tracking_active = False
        self.agent_name = None
        self._committed_form_state: dict[str, object] | None = None
        self._has_unsaved_form_changes = False
        self._is_restoring_form_state = False

        load_style('resources/styles/stint_tracking/tracker/config_options.qss', widget=self)

        self.selection_model.view_change_guard = self._can_switch_views
        self.selection_model.eventChanged.connect(self._refresh_labels)
        self.selection_model.sessionChanged.connect(self._refresh_labels)

        self._setup_ui()
        self._refresh_labels()

    def closeEvent(self, event):
        try:
            self.selection_model.view_change_guard = None
            self._shutdown_tracking()
        except Exception as e:
            log_exception(e, 'Error in ConfigOptions.closeEvent during _shutdown_tracking',
                category='ui', action='ConfigOptions.closeEvent')
        super().closeEvent(event)

    def _open_popup(self, title: str, message: str, buttons: list[str], type: str = "info"):
        dialog = PopUp(
            title=title,
            message=message,
            buttons=buttons,
            type=type,
            parent=self,
        )
        dialog.exec()
