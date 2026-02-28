"""
Stint Tracker - Main entry point.

Independent process that monitors LMU game state and creates stint records
when pit stops are detected. Runs continuously until stopped by the UI.

Usage:
    python run.py --session-id <id> --drivers <names> [--practice]

Additional options:
    --agent-name    custom name for this tracker instance
    --dry-run       run loop without reading LMU data; heartbeats & cleanup still occur
"""

import sys
from pathlib import Path

# insert project root to sys.path early so submodules can be imported
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from core.errors import log, log_exception
from processors.stint_tracker.core.track_session import track_session
from processors.stint_tracker.helpers import (
    _parse_args,
    _register_tracker_agent,
    _unregister_tracker_agent,
    _open_lmu_shared_memory,
)


def main() -> None:
    """High‑level orchestration for the stint tracker process.

    The function reads CLI arguments, registers the agent, and then
    either opens the LMU shared memory or runs in dry mode. An assertion
    ensures the registration produced a non‑empty name.
    """
    args = _parse_args()
    agent_name = _register_tracker_agent(args.agent_name)
    assert agent_name, "Tracker agent name must be non‑empty"

    try:
        if args.dry_run:
            log(
                "INFO",
                "Dry-run mode enabled; skipping LMU memory access",
                category="stint_tracker",
                action="main",
            )
            track_session(
                None,
                None,
                session_id=args.session_id,
                drivers=args.drivers,
                is_practice=args.practice,
                agent_name=agent_name,
                dry_run=True,
            )
        else:
            # open shared memory safely with context manager
            with _open_lmu_shared_memory() as lmu:
                track_session(
                    lmu_telemetry=lmu.telemetry,
                    lmu_scoring=lmu.scoring,
                    session_id=args.session_id,
                    drivers=args.drivers,
                    is_practice=args.practice,
                    agent_name=agent_name,
                    dry_run=False,
                )

    except KeyboardInterrupt:
        log('INFO', 'Stint tracker stopped by user',
            category='stint_tracker', action='main')
        sys.exit(0)
    except Exception as e:  # pylint: disable=broad-except
        log_exception(e, 'Fatal error in stint tracker',
                     category='stint_tracker', action='main')
        print(f"__error__:stint_tracker:{str(e)}", file=sys.stderr)
        sys.exit(1)
    finally:
        # ensure agent is removed whether we exit normally or on error
        if agent_name:
            _unregister_tracker_agent(agent_name)


if __name__ == '__main__':
    main()
