from core.database import update_agent_heartbeat

def _maybe_update_heartbeat(agent_name: str | None) -> None:
    """Update the agent heartbeat in the database (non-fatal).

    Silently logs debug on failure so the tracker loop can continue.
    """
    if not agent_name:
        return

    try:
        update_agent_heartbeat(agent_name)
    except Exception:
        log("DEBUG", f"Failed to update heartbeat for {agent_name}",
            category='stint_tracker', action='heartbeat_update')