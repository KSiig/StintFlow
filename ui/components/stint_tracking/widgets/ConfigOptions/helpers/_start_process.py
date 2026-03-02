from __future__ import annotations

from PyQt6.QtCore import QProcess

from core.errors import log, log_exception
from core.utilities import get_stint_tracker_command, load_user_settings


def _start_process(self) -> None:
    """Launch the stint_tracker subprocess."""
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
            '--drivers', *self.drivers,
        ]
        try:
            settings = load_user_settings()
            if isinstance(settings, dict):
                agent_name = settings.get('agent', {}).get('name')
            else:
                try:
                    import socket

                    agent_name = socket.gethostname()
                except Exception:
                    agent_name = None
            if agent_name:
                process_args += ['--agent-name', agent_name]
        except Exception:
            agent_name = None

        self.agent_name = agent_name

        if is_practice:
            process_args.append('--practice')

        self.p.start(program, process_args)
        if not self.p.waitForStarted():
            error_message = self.p.errorString()
            log('ERROR', f'Failed to start stint tracker: {error_message}', category='config_options', action='start_process')
            self._revert_tracking_state()
            self.p = None
            return

        self._tracking_active = True
        log('INFO', f'Started stint tracker process: {program} {process_args}', category='config_options', action='start_process')
    except Exception as e:
        log_exception(e, 'Failed to start stint tracker process', category='config_options', action='start_process')
