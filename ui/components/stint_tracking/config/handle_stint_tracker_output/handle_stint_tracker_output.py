"""Parse and dispatch messages from the stint_tracker subprocess.

The tracker process writes structured log lines to stdout/stderr which
indicate events such as stunt creation, garage entry/exit, or errors like
registration conflicts.  This module provides a single function,
``handle_stint_tracker_output``, which inspects the text and invokes one of
several optional callbacks supplied by the caller.

Callbacks:

- ``on_stint_created``: invoked when a new stint is recorded.
- ``on_return_to_garage``: triggered when the player is asked to return
  to garage.
- ``on_player_in_garage``: called when the player has been detected in
  the garage.
- ``on_no_active_vehicles``: fired when the tracker cannot find any
  active vehicles in the session.
- ``on_registration_conflict``: executed when the tracker reports an
  agent-name collision.
"""

from core.errors import log, log_exception


def handle_stint_tracker_output(
    stdout: str,
    on_stint_created=None,
    on_return_to_garage=None,
    on_player_in_garage=None,
    on_registration_conflict=None,
) -> None:
    """Parse structured event messages from the stint_tracker process."""
    try:
        message = stdout.strip()
        if message:
            log("INFO", message, category="stint_tracker", action="process_output")

        if ": [stint_tracker:" in stdout:
            if "[stint_tracker:create_stint]" in stdout and any(marker in stdout for marker in ("Created stint", "Deduped stint")):
                if on_stint_created:
                    on_stint_created()
            elif "[stint_tracker:track_session]" in stdout and "return to garage" in stdout.lower():
                if on_return_to_garage:
                    on_return_to_garage()
            elif "[stint_tracker:track_session]" in stdout and "in garage" in stdout.lower():
                if on_player_in_garage:
                    on_player_in_garage()

        if ": [database:" in stdout:
            if "[database:register_agent]" in stdout and "agent already exists" in stdout.lower():
                if on_registration_conflict:
                    on_registration_conflict()
            if "[database:set_tires_remaining_at_green_flag]" in stdout and "set tires remaining at green flag" in stdout.lower():
                # Reuse on_stint_created callback to trigger UI update after setting tires_remaining_at_green_flag
                if on_stint_created:
                    on_stint_created()
    except Exception as exc:
        log_exception(exc, f"Failed to parse output: {stdout}", category="config_options", action="handle_output")
