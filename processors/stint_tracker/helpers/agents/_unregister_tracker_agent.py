from core.database import register_agent, delete_agent
from core.errors import log, log_exception

def _unregister_tracker_agent(agent_name: str) -> None:
    """Try to delete the agent entry, ignoring any errors.

    Logs at DEBUG level if deletion fails.
    """
    try:
        delete_agent(agent_name)
        log('DEBUG', f'Agent {agent_name} unregistered',
            category='stint_tracker', action='agent_registration')
    except Exception as e:
        log('DEBUG', f'Failed to unregister agent {agent_name}: {e}',
            category='stint_tracker', action='agent_registration')