"""
Parse and handle stint tracker process output.

Processes structured event messages from the stint_tracker process.
"""

from core.errors import log, log_exception


def handle_stint_tracker_output(stdout: str, on_stint_created=None, 
                                on_return_to_garage=None, on_player_in_garage=None):
    """
    Parse structured event messages from stint_tracker.
    
    Args:
        stdout: Event message in format __event__:process:message or log format
        on_stint_created: Callback function when stint is created
        on_return_to_garage: Callback function when player should return to garage
        on_player_in_garage: Callback function when player is in garage
    """
    try:
        message = stdout.strip()
        if message:
            log('INFO', message, category='stint_tracker', action='process_output')
        
        # Handle log format: "INFO: [category:action] message"
        if ': [stint_tracker:' in stdout:
            # Parse structured log messages
            if '[stint_tracker:create_stint]' in stdout and any(
                marker in stdout for marker in ('Created stint', 'Deduped stint')
            ):
                if on_stint_created:
                    on_stint_created()
            elif '[stint_tracker:track_session]' in stdout and 'return to garage' in stdout.lower():
                if on_return_to_garage:
                    on_return_to_garage()
            elif '[stint_tracker:track_session]' in stdout and 'in garage' in stdout.lower():
                if on_player_in_garage:
                    on_player_in_garage()
    
    except Exception as e:
        log_exception(e, f'Failed to parse output: {stdout}',
                     category='config_options', action='handle_output')
