"""
Configuration options widget for stint tracking.

Displays event/session configuration with editable fields and tracking controls.
Launches the stint_tracker process and communicates via stdout/stderr events.
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame,
    QCheckBox, QLineEdit, QLabel, QApplication
)
from PyQt6.QtCore import Qt, pyqtSignal, QProcess
from datetime import datetime

from .TeamSection import TeamSection
from ui.models import ModelContainer
from ui.utilities import get_fonts, FONT
from core.utilities import resource_path, get_stint_tracker_command, load_user_settings
from core.database import (
    get_event, get_session, get_sessions, get_team,
    update_event, update_session, update_team_drivers,
    create_event, create_session, delete_agent
)
from core.errors import log, log_exception
from ..config import (
    ConfigLayout, ConfigLabels,
    handle_stint_tracker_output
)
from ui.components.common import SectionHeader, LabeledInputRow, ConfigButton, PopUp


class ConfigOptions(QWidget):
    """
    Configuration panel for stint tracking.
    
    Displays event configuration (name, tires, length), session details,
    driver names, and tracking controls. Manages the stint_tracker process.
    
    Signals:
        stint_created: Emitted when stint_tracker reports a new stint
    """
    
    stint_created = pyqtSignal()
    tracker_started = pyqtSignal()
    tracker_stopped = pyqtSignal()
    
    def __init__(self, models: ModelContainer):
        """
        Initialize configuration options widget.
        
        Args:
            models: Container with selection_model and table_model
        """
        super().__init__()
        
        self.selection_model = models.selection_model
        self.table_model = models.table_model
        self.event = None
        self.session = None
        self.team = None
        self.drivers = []
        self.inputs = {}
        self.driver_inputs = []  # List of QLineEdit, not dict
        self.p = None  # QProcess for stint_tracker
        self._tracking_active = False
        
        # Load stylesheet
        try:
            with open(resource_path('resources/styles/config_options.qss'), 'r') as f:
                self.setStyleSheet(f.read())
        except Exception as e:
            log_exception(e, 'Failed to load config_options stylesheet',
                         category='ui', action='load_stylesheet')
        
        # Connect to selection model signals
        self.selection_model.eventChanged.connect(self._refresh_labels)
        self.selection_model.sessionChanged.connect(self._refresh_labels)
        
        self._setup_ui()
        self._refresh_labels()
    
    def closeEvent(self, event):
        """Clean up QProcess on widget close."""
        if self.p and self.p.state() == QProcess.ProcessState.Running:
            self.p.kill()
            self.p.waitForFinished()
        super().closeEvent(event)
    
    def _setup_ui(self):
        """Build the UI layout with all configuration fields."""
        # Main frame
        frame = QFrame()
        frame.setObjectName("ConfigOptions")
        frame.setFixedWidth(ConfigLayout.FRAME_WIDTH)
        
        root_widget_layout = QVBoxLayout(self)
        root_widget_layout.setContentsMargins(0, 0, 0, 0)
        root_widget_layout.addWidget(frame)
        
        # Create all buttons and controls
        self._create_buttons()
        
        # Main layout
        root_layout = QVBoxLayout(frame)
        root_layout.setContentsMargins(0, 0, ConfigLayout.RIGHT_MARGIN, 0)
        root_layout.setSpacing(ConfigLayout.CONTENT_SPACING)
        
        # Add header using SectionHeader widget
        header = SectionHeader(
            title="Race Configuration",
            icon_path="resources/icons/race_config/settings.svg",
            icon_color="#05fd7e",
            icon_size=ConfigLayout.ICON_SIZE,
            spacing=ConfigLayout.HEADER_SPACING
        )
        root_layout.addWidget(header)
        
        # Add configuration rows
        self._add_config_rows(root_layout)
        
        # Add buttons
        root_layout.addLayout(self._create_button_layout())
        
        self.save_btn.hide()
        self.stop_btn.hide()
        root_layout.addStretch()
    
    def _add_config_rows(self, layout: QVBoxLayout):
        """Add all configuration row widgets to layout."""
        # Create and store input field references
        for field_id, title in [
            ("event_name", "Event name"),
            ("session_name", "Session name"),
            ("tires", "Starting tires"),
            ("length", "Race length"),
            ("start_time", "Start time")
        ]:
            card = LabeledInputRow(title=title, input_height=ConfigLayout.INPUT_HEIGHT)
            self.inputs[field_id] = card.get_input_field()
            layout.addWidget(card)
        
        # Add team/driver section
        self.team_section = TeamSection()
        self.team_section._set_active(False)  # Start with add/remove buttons disabled
        self.driver_inputs = self.team_section.get_driver_inputs()
        self.drivers = self.team_section.get_driver_names()
        layout.addWidget(self.team_section)
    
    def _create_buttons(self):
        """Create all buttons and controls."""
        # Action buttons
        self.edit_btn = ConfigButton(ConfigLabels.BTN_EDIT, icon_path="resources/icons/race_config/square-pen.svg")
        self.save_btn = ConfigButton(ConfigLabels.BTN_SAVE, icon_path="resources/icons/race_config/square-pen.svg")
        self.clone_btn = ConfigButton(ConfigLabels.BTN_CLONE, icon_path="resources/icons/race_config/copy.svg")
        self.create_session_btn = ConfigButton(ConfigLabels.BTN_NEW_SESSION, width_type="full")
        self.start_btn = ConfigButton(ConfigLabels.BTN_START_TRACK, icon_path="resources/icons/race_config/play.svg", icon_color="#1E1F24")
        self.stop_btn = ConfigButton(ConfigLabels.BTN_STOP_TRACK, icon_path="resources/icons/race_config/play.svg", icon_color="#1E1F24")
        self.start_btn.setObjectName("TrackButton")
        self.stop_btn.setObjectName("TrackButton")
        
        # Practice checkbox and warning label
        self.practice_cb = QCheckBox(text="Practice")
        self.lbl_info = QLabel()
        self.practice_cb.setFont(get_fonts(FONT.input_field))
        self.lbl_info.setFont(get_fonts(FONT.header_input))
        self.lbl_info.setObjectName("InfoLabel")
        self.lbl_info.hide()
        
        # Connect button signals
        self.edit_btn.clicked.connect(self._toggle_edit)
        self.save_btn.clicked.connect(lambda: (self._save_config(), self._toggle_edit()))
        self.clone_btn.clicked.connect(self._clone_event)
        self.create_session_btn.clicked.connect(self._create_session)
        self.stop_btn.clicked.connect(self._toggle_track)
        self.start_btn.clicked.connect(self._toggle_track)
    
    def _create_button_layout(self) -> QHBoxLayout:
        """Create the button layout with all controls."""
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(ConfigLayout.BUTTON_SPACING)
        
        # Top column: edit/save/clone buttons
        btn_layout_save_clone = QHBoxLayout()
        btn_layout_save_clone.addWidget(self.edit_btn, alignment=Qt.AlignmentFlag.AlignTop)
        btn_layout_save_clone.addWidget(self.save_btn, alignment=Qt.AlignmentFlag.AlignTop)
        btn_layout_save_clone.addWidget(self.clone_btn, alignment=Qt.AlignmentFlag.AlignTop)
        btn_layout_save_clone.addWidget(self.start_btn, alignment=Qt.AlignmentFlag.AlignTop)
        btn_layout_save_clone.addWidget(self.stop_btn, alignment=Qt.AlignmentFlag.AlignTop)
        
        # Right column: tracking controls
        btn_tracking_layout = QVBoxLayout()
        btn_tracking_layout.setSpacing(8)
        btn_tracking_layout.addWidget(self.create_session_btn, alignment=Qt.AlignmentFlag.AlignTop)
        btn_tracking_layout.addWidget(self.lbl_info, alignment=Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)
        btn_tracking_layout.addStretch()
        
        btn_layout.addWidget(self.practice_cb)
        btn_layout.addLayout(btn_layout_save_clone)
        btn_layout.addLayout(btn_tracking_layout)
        
        return btn_layout
    
    def _refresh_labels(self):
        """Reload event/session data and update input fields."""
        try:
            # Load event data
            self.event = get_event(self.selection_model.event_id)
            if not self.event:
                log('WARNING', 'No event found for current selection',
                    category='config_options', action='refresh_labels')
                return
            
            # Load session data
            self.session = get_session(self.selection_model.session_id)
            if not self.session:
                # Fall back to last session for this event
                sessions = list(get_sessions(self.event['_id']))
                if sessions:
                    self.session = sessions[-1]
                    self.selection_model.set_session(
                        str(self.session['_id']),
                        self.session['name']
                    )
            
            # Reload team data to pick up driver changes
            self.team = get_team()
            if self.team:
                self.drivers = self.team.get('drivers', [])
                # Update driver input fields if they exist
                for i, driver in enumerate(self.drivers):
                    if i < len(self.driver_inputs):
                        self.driver_inputs[i].setText(driver)
            
            # Update input fields
            if self.event:
                self.inputs['event_name'].setText(self.event.get('name', ''))
                self.inputs['tires'].setText(str(self.event.get('tires', '')))
                self.inputs['length'].setText(self.event.get('length', ''))
                self.inputs['start_time'].setText(self.event.get('start_time', ''))
            
            if self.session:
                self.inputs['session_name'].setText(self.session.get('name', ''))
        
        except Exception as e:
            log_exception(e, 'Failed to refresh configuration labels',
                         category='config_options', action='refresh_labels')
    
    def _toggle_edit(self):
        """Toggle between edit and view modes for configuration fields."""
        # Edit mode -> View mode
        if self.save_btn.isVisible():
            self.save_btn.hide()
            self.edit_btn.show()
            self.team_section._set_active(False)  # Disable add/remove buttons
            for child in self.findChildren(QLineEdit):
                child.setReadOnly(True)
                child.setProperty('editable', False)
                child.style().unpolish(child)
                child.style().polish(child)
        # View mode -> Edit mode
        else:
            self.edit_btn.hide()
            self.save_btn.show()
            self.team_section._set_active(True)  # Enable add/remove buttons
            for child in self.findChildren(QLineEdit):
                child.setReadOnly(False)
                child.setProperty('editable', True)
                child.style().unpolish(child)
                child.style().polish(child)
    
    def _save_config(self):
        """Save configuration changes to database."""
        try:
            # Update event
            update_event(
                str(self.selection_model.event_id),
                name=self.inputs['event_name'].text(),
                tires=self.inputs['tires'].text(),
                length=self.inputs['length'].text(),
                start_time=self.inputs['start_time'].text()
            )
            
            # Update session
            update_session(
                str(self.selection_model.session_id),
                name=self.inputs['session_name'].text()
            )
            
            # Update drivers
            drivers = [line_edit.text() for line_edit in self.driver_inputs]
            if self.team:
                update_team_drivers(str(self.team['_id']), drivers)
                self.drivers = drivers  # Update local driver list
            
            # Refresh table
            self.table_model.update_data()
            
            log('INFO', 'Configuration saved successfully',
                category='config_options', action='save_config')
        
        except Exception as e:
            log_exception(e, 'Failed to save configuration',
                         category='config_options', action='save_config')
    
    def _clone_event(self):
        """Clone current event and create a new session."""
        try:
            # Clone event (remove _id to create new document)
            event_data = dict(self.event)
            if '_id' in event_data:
                del event_data['_id']
            event_data['name'] = event_data.get('name', 'Event') + " - Clone"
            
            result = create_event(event_data)
            if not result:
                log('ERROR', 'Failed to create cloned event',
                    category='config_options', action='clone_event')
                return
            
            # Create practice session for new event
            session_data = {
                "race_id": result.inserted_id,
                "name": "practice"
            }
            session_result = create_session(session_data)
            if not session_result:
                log('ERROR', 'Failed to create session for cloned event',
                    category='config_options', action='clone_event')
                return
            
            # Update selection to new event/session
            new_event = get_event(str(result.inserted_id))
            new_session = get_session(str(session_result.inserted_id))
            
            if new_event and new_session:
                self.selection_model.set_event(str(new_event['_id']), new_event['name'])
                self.selection_model.set_session(str(new_session['_id']), new_session['name'])
            
            log('INFO', 'Event cloned successfully',
                category='config_options', action='clone_event')
        
        except Exception as e:
            log_exception(e, 'Failed to clone event',
                         category='config_options', action='clone_event')
    
    def _create_session(self):
        """Create a new session for the current event."""
        try:
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            session_name = "Practice - " + now
            
            session_data = {
                "race_id": self.event['_id'],
                "name": session_name
            }
            
            result = create_session(session_data)
            if not result:
                log('ERROR', 'Failed to create new session',
                    category='config_options', action='create_session')
                return
            
            # Update selection to new session
            self.selection_model.set_session(str(result.inserted_id), session_name)
            
            log('INFO', f'Created new session: {session_name}',
                category='config_options', action='create_session')
        
        except Exception as e:
            log_exception(e, 'Failed to create session',
                         category='config_options', action='create_session')
    
    def _toggle_track(self):
        """Toggle stint tracking on/off."""
        # Start tracking
        if self.stop_btn.isHidden():
            self.start_btn.hide()
            self.stop_btn.show()
            self._start_process()
            self.tracker_started.emit()
        # Stop tracking
        else:
            self._revert_tracking_state()
            self._tracking_active = False
            if self.p:
                self.p.kill()
                self.p = None
            self.tracker_stopped.emit()
    def _start_process(self):
        """Launch the stint_tracker process."""
        try:
            self.p = QProcess()
            self.p.readyReadStandardOutput.connect(self._handle_stdout)
            self.p.readyReadStandardError.connect(self._handle_stderr)
            self.p.errorOccurred.connect(self._handle_process_error)
            self.p.finished.connect(self._handle_process_finished)
            
            is_practice = self.practice_cb.isChecked()
            program, process_args = get_stint_tracker_command()
            process_args += [
                '--session-id', str(self.selection_model.session_id),
                '--drivers', *self.drivers
            ]
            # add optional agent name if user configured one
            try:
                settings = load_user_settings()
                if isinstance(settings, dict):
                    agent_name = settings.get('agent', {}).get('name')
                else:
                    # Avoid importing heavy modules at top‑level since this method is
                    # only called from the settings view.  ``socket.gethostname`` is the
                    # most reliable cross‑platform way to obtain the device name.
                    try: 
                        import socket
                        agent_name = socket.gethostname()
                    except Exception:
                        agent_name = None
                if agent_name:
                    process_args += ['--agent-name', agent_name]
            except Exception:
                # ignore errors reading settings; fall back to default behaviour
                pass
                agent_name = None

            self.agent_name = agent_name  # Store for later use in error handling

            if is_practice:
                process_args.append('--practice')
            
            self.p.start(program, process_args)
            if not self.p.waitForStarted():
                error_message = self.p.errorString()
                log('ERROR', f'Failed to start stint tracker: {error_message}',
                    category='config_options', action='start_process')
                self._revert_tracking_state()
                self.p = None
                return

            self._tracking_active = True
            log('INFO', f'Started stint tracker process: {program} {process_args}',
                category='config_options', action='start_process')
        
        except Exception as e:
            log_exception(e, 'Failed to start stint tracker process',
                         category='config_options', action='start_process')
    
    def _handle_stderr(self):
        """Handle stderr output from stint_tracker process."""
        if not self.p:
            return
        
        data = self.p.readAllStandardError()
        stderr = bytes(data).decode("utf8")
        self._handle_output(stderr)  # Attempt to parse structured events from stderr as well
        log('ERROR', f'Stint tracker stderr: {stderr}',
            category='config_options', action='handle_stderr')
    
    def _handle_stdout(self):
        """Handle stdout output from stint_tracker process."""
        if not self.p:
            return
        
        data = self.p.readAllStandardOutput()
        stdout = bytes(data).decode("utf8")
        
        self._handle_output(stdout)
    
    def _handle_output(self, stdout: str):
        """
        Parse structured event messages from stint_tracker.
        
        Args:
            stdout: Event message in format __event__:process:message
        """
        handle_stint_tracker_output(
            stdout,
            on_stint_created=lambda: self.stint_created.emit(),
            on_return_to_garage=lambda: self._show_info_lbl("Please return to garage!"),
            on_player_in_garage=self._reset_info_lbl,
            on_registration_conflict=self._handle_agent_registration_conflict
        )

    def _show_info_lbl(self, text):
        """Show return to garage warning and flash taskbar icon."""
        self.lbl_info.show()
        self.lbl_info.setText(text)
        self._flash_taskbar()

    def _reset_info_lbl(self):
        """Hide return to garage warning."""
        self.lbl_info.setText("")
        self.lbl_info.hide()

    def _handle_agent_registration_conflict(self):
        """Handle agent name conflict by showing a warning."""
        dialog = PopUp(
            title="Agent name conflict",
            message="Agent name conflict detected! Please choose a different name in settings.",
            buttons=["Ok"],
            type="error",
            parent=self
        )
        dialog.exec()
        self._toggle_track() # Stop the process since it won't function properly with a registration conflict

    def _flash_taskbar(self):
        """Request taskbar icon attention (flash orange on Windows) using QApplication.alert."""
        window = self.window()
        if window:
            QApplication.alert(window, 0)

    def _handle_process_error(self, error):
        """Handle process-level errors and revert the UI state."""
        if not self.p:
            return

        error_message = self.p.errorString()
        log('ERROR', f'Stint tracker process error: {error_message}',
            category='config_options', action='process_error')
        if self._tracking_active:
            self._revert_tracking_state()
            self.p = None

    def _handle_process_finished(self, exit_code, exit_status):
        """Handle process exit to keep UI state in sync."""
        if not self._tracking_active:
            return

        log('WARNING', f'Stint tracker exited: code={exit_code}, status={exit_status}',
            category='config_options', action='process_finished')
        self._revert_tracking_state()
        self.p = None

    def _revert_tracking_state(self):
        """Revert tracking UI state if the process fails to start."""
        self.stop_btn.hide()
        self.start_btn.show()
        self.lbl_info.hide()
        delete_agent(self.agent_name)  # Attempt to clean up agent registration on failure
