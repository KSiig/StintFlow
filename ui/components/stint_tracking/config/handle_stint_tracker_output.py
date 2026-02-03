"""
Parse and handle stint tracker process output.

Processes structured event messages from the stint_tracker process.
"""

from core.errors import log_exception


def handle_stint_tracker_output(stdout: str, on_stint_created=None, 
                                on_return_to_garage=None, on_player_in_garage=None):
    """
    Parse structured event messages from stint_tracker.
    
    Args:
        stdout: Event message in format __event__:process:message
        on_stint_created: Callback function when stint is created
        on_return_to_garage: Callback function when player should return to garage
        on_player_in_garage: Callback function when player is in garage
    """
    try:
        args = stdout.split(':')
        if len(args) < 3:
            return
        
        event_type = args[0].strip()
        process = args[1].strip()
        msg = args[2].strip()
        
        if event_type == '__event__':
            if process == 'stint_tracker':
                if msg == 'stint_created' and on_stint_created:
                    on_stint_created()
        
        elif event_type == '__info__':
            if process == 'stint_tracker':
                if msg == 'return_to_garage' and on_return_to_garage:
                    on_return_to_garage()
                elif msg == 'player_in_garage' and on_player_in_garage:
                    on_player_in_garage()
    
    except Exception as e:
        log_exception(e, f'Failed to parse output: {stdout}',
                     category='config_options', action='handle_output')
