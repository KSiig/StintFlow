from core.database import clean_stale_agents
import time
from core.errors import log

CLEANUP_INTERVAL: float = 5.0  # seconds between stale-agent cleanup attempts
STALE_THRESHOLD: int = 60  # grace period passed to cleanup function

def _maybe_cleanup_stale_agents(last_cleanup: float) -> float:
    """Run stale-agent cleanup if the configured interval elapsed.

    Returns the updated last_cleanup timestamp.
    """
    now = time.time()
    if now - last_cleanup < CLEANUP_INTERVAL:
        return last_cleanup

    try:
        clean_stale_agents(grace_period_seconds=STALE_THRESHOLD)
    except Exception:
        log("DEBUG", "Error while cleaning stale agents",
            category='stint_tracker', action='cleanup_stale_agents')
    return now