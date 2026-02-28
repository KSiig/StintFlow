from core.database import register_agent
from core.errors import log

def _register_tracker_agent(agent_name: str) -> str:
    """Attempt to register an agent and log the outcome.

    Returns the final name assigned/used by the database (may differ if
    the original name collided).
    """
    try:
        registered, final_name = register_agent(agent_name)
        if registered:
            log('INFO', f'Agent registered as {final_name}',
                category='stint_tracker', action='agent_registration')
        else:
            log('WARNING',
                f'Agent name already in use: "{final_name}"; '
                'tracking will continue but duplicate names may confuse UI',
                category='stint_tracker', action='agent_registration')
        return final_name
    except Exception:
        log('WARNING', f'Failed to register agent {agent_name}',
            category='stint_tracker', action='agent_registration')
        # fall back to whatever name was supplied (or empty string)
        return agent_name or ""