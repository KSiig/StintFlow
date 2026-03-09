"""Parse and handle stint tracker process output."""

from core.errors import log, log_exception


def handle_stint_tracker_output(
    stdout: str,
    on_stint_created=None,
    on_return_to_garage=None,
    on_player_in_garage=None,
    on_no_active_vehicles=None,
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
            elif "[stint_tracker:find_player]" in stdout and "no active vehicles in session" in stdout.lower():
                if on_no_active_vehicles:
                    on_no_active_vehicles()

        if ": [database:" in stdout:
            if "[database:register_agent]" in stdout and "agent already exists" in stdout.lower():
                if on_registration_conflict:
                    on_registration_conflict()
    except Exception as exc:
        log_exception(exc, f"Failed to parse output: {stdout}", category="config_options", action="handle_output")
