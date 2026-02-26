"""
Stint Tracker - Main entry point.

Independent process that monitors LMU game state and creates stint records
when pit stops are detected. Runs continuously until stopped by the UI.

Usage:
    python run.py --session-id <id> --drivers <names> [--practice]
"""

import sys
from pathlib import Path

# Add project root to sys.path to access pyLMUSharedMemory and core modules
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

import argparse
import mmap
import ctypes
import os
from datetime import datetime
from pyLMUSharedMemory import lmu_data
from core.errors import log, log_exception
from core.database import register_agent, delete_agent
from processors.stint_tracker.core.track_session import track_session

def main():
    """Parse arguments and start stint tracking."""
    parser = argparse.ArgumentParser(
        description="Track stints by monitoring LMU shared memory"
    )
    
    parser.add_argument(
        "--session-id",
        required=True,
        help="ID of session to create stints in"
    )
    
    parser.add_argument(
        "--drivers",
        nargs="+",
        required=True,
        help="List of driver names for this session"
    )
    
    parser.add_argument(
        "--practice",
        action="store_true",
        help="Practice mode - requires player to return to garage before tracking"
    )

    parser.add_argument(
        "--agent-name",
        help="Optional unique name for this tracker instance. If omitted a default based on host name will be used."
    )
    
    args = parser.parse_args()
    
    # determine agent name and register in database
    agent_name = args.agent_name
    try:
        registered, agent_name = register_agent(agent_name)
        if registered:
            log('INFO', f'Agent registered as {agent_name}',
                category='stint_tracker', action='agent_registration')
        else:
            # registration returned False: often means name already exists
            log('WARNING',
                f'Agent name already in use: "{agent_name}"; ' \
                'tracking will continue but duplicate names may confuse UI',
                category='stint_tracker', action='agent_registration')
    except Exception:
        # unexpected errors shouldn't prevent tracking
        log('WARNING', f'Failed to register agent {agent_name}',
            category='stint_tracker', action='agent_registration')
    
    try:
        # Open LMU shared memory
        shared_mem = mmap.mmap(
            fileno=0,
            length=ctypes.sizeof(lmu_data.LMUObjectOut),
            tagname=lmu_data.LMUConstants.LMU_SHARED_MEMORY_FILE
        )
        
        lmu = lmu_data.LMUObjectOut.from_buffer(shared_mem)
        
        # Start tracking
        log('INFO', f'Starting stint tracker for session {args.session_id}',
            category='stint_tracker', action='main')
        
        track_session(
            lmu_telemetry=lmu.telemetry,
            lmu_scoring=lmu.scoring,
            session_id=args.session_id,
            drivers=args.drivers,
            is_practice=args.practice,
            agent_name=agent_name,
        )
        # while True:
        #     print("next loop")
        #     time.sleep(1)
        
    except KeyboardInterrupt:
        log('INFO', 'Stint tracker stopped by user',
            category='stint_tracker', action='main')
        # unregister agent if possible
        try:
            delete_agent(agent_name)
        except Exception:
            pass
        sys.exit(0)
        
    except Exception as e:
        log_exception(e, 'Fatal error in stint tracker',
                     category='stint_tracker', action='main')
        print(f"__error__:stint_tracker:{str(e)}", file=sys.stderr)
        delete_agent(agent_name)
        sys.exit(1)


if __name__ == '__main__':
    main()
