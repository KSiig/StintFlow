# Stint Tracker Processor

Independent OS process that monitors LMU (Le Mans Ultimate) shared memory and creates stint records when pit stops are detected.

## Overview

The stint tracker runs as a standalone Python process, separate from the main UI application. It continuously monitors the game state via LMU's shared memory interface and automatically creates database records when it detects completed pit stops.

## Architecture

```
processors/stint_tracker/
├── run.py                      # Entry point (run as OS process)
├── core/                       # Core tracking logic
│   ├── track_session.py       # Main monitoring loop
│   ├── create_stint.py        # Database record creation
│   └── calculate_remaining_time.py  # Time calculations
├── pit_detection/             # Pit state monitoring
│   ├── pit_state.py          # Pit state enum and detection
│   └── find_player.py        # Player vehicle identification
└── tire_management/           # Tire tracking
    ├── get_tire_state.py     # Complete tire state extraction
    ├── get_tire_wear.py      # Wear calculation
    ├── get_tire_compound.py  # Compound detection
    └── detect_tire_changes.py # Change detection
```

## Usage

### From UI (Recommended)
The UI automatically launches this processor when "Track" button is clicked.

### Manual Launch
```bash
python processors/stint_tracker/run.py \
  --session-id <mongodb_session_id> \
  --drivers "Driver 1" "Driver 2" \
  [--practice]
```

### Arguments

- `--session-id`: MongoDB ObjectId of the session to track
- `--drivers`: Space-separated list of driver names to monitor
- `--practice`: Optional flag for practice mode (requires return to garage before tracking)
- `--agent-name`: Optional string to uniquely identify this tracker process.  When
  provided (or a default generated from the PID) the tracker will register
  itself in the ``agents`` collection and periodically update a heartbeat so
  that the UI can display currently connected agents (see issue #59).  This
  value can also be configured persistently via the Settings view ("Tracker
  agent" field) or by setting the `AGENT_NAME` environment variable; the UI
  automatically passes the stored name when starting the processor.

## Communication Protocol

The processor communicates with the UI via stdout using structured event messages:

### Events
- `__event__:stint_tracker:stint_created` - New stint record created
- `__info__:stint_tracker:return_to_garage` - Practice mode: waiting for garage return
- `__info__:stint_tracker:player_in_garage` - Player is in garage
- `__error__:stint_tracker:<message>` - Error occurred (via stderr)

## How It Works

1. **Initialization**
   - Opens LMU shared memory
   - Loads previous stints (for practice mode)
   - Begins monitoring loop at 1Hz

2. **Main Loop**
   - Monitors pit state transitions
   - Captures tire state when entering pits
   - Detects pit stop completion (LEAVING state)
   - Calculates remaining race time
   - Creates stint record with tire data

3. **Practice Mode**
   - Waits for player to return to garage before tracking
   - Calculates time based on previous stint
   - Allows for interrupted sessions

4. **Stint Creation**
   - Compares incoming/outgoing tire states
   - Detects tire changes based on wear levels
   - Skips recording if penalty was served
   - Emits event to notify UI

## Database Schema

Stint documents created by this processor:

```python
{
    "session_id": ObjectId,        # Reference to session
    "driver": str,                 # Driver name
    "pit_end_time": str,          # HH:MM:SS format
    "tire_data": {
        "fl": {                    # Front left (also fr, rl, rr)
            "incoming": {
                "wear": float,     # 0.0 - 1.0
                "flat": int,       # Boolean flag
                "detached": int,   # Boolean flag
                "compound": str    # Tire compound type
            },
            "outgoing": { ... }    # Same structure
        },
        "tires_changed": {         # Which tires were changed
            "fl": bool,
            "fr": bool,
            "rl": bool,
            "rr": bool
        }
    }
}
```

## Dependencies

- **pyLMUSharedMemory**: LMU shared memory interface (submodule)
- **pymongo**: Database operations (via core.database)
- **core.errors**: Logging and error handling

## Troubleshooting

**Process won't start**
- Check LMU is running with shared memory enabled
- Verify session_id exists in database
- Ensure Python has access to shared memory

**No stints being created**
- Check driver names match exactly (case-sensitive)
- Verify pit stop is completing normally (not penalty lap)
- Look for errors in stderr output

**Incorrect times in practice mode**
- Ensure previous stint times are valid
- Check that player returned to garage before first stint
