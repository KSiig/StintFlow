"""
Helper functions for stint table calculations.

Utility functions for converting stint types, calculating stint lengths,
and managing tire data.
"""

from datetime import datetime, date, timedelta, time

def get_stint_type(stint_amount: int) -> str:
    """
    Convert stint count to stint type name.
    
    Args:
        stint_amount: Number of laps/segments in stint (1-10+)
        
    Returns:
        String name like "Single", "Double", "Triple", etc.
    """
    mapping = {
        0: "Single",
        1: "Double",
        2: "Triple",
        3: "Quadruple",
        4: "Quintuple",
        5: "Sextuple",
        6: "Septuple",
        7: "Octuple",
        8: "Nonuple",
        9: "Decuple",
    }
    return mapping.get(stint_amount, "Unknown")


def get_stint_length(stint_type: str) -> int:
    """
    Convert stint type name to numeric length.
    
    Args:
        stint_type: Stint type like "Single", "Double", etc.
        
    Returns:
        Integer length (1-10), defaults to 1 if unknown
    """
    if not stint_type:
        return 1
    
    mapping = {
        "Single": 1,
        "Double": 2,
        "Triple": 3,
        "Quadruple": 4,
        "Quintuple": 5,
        "Sextuple": 6,
        "Septuple": 7,
        "Octuple": 8,
        "Nonuple": 9,
        "Decuple": 10,
    }
    return mapping.get(stint_type, 1)


def get_default_tire_dict(tires_changed: bool) -> dict:
    """
    Create default tire data dictionary.
    
    Args:
        tires_changed: Whether all tires are marked as changed
        
    Returns:
        Dictionary with tire data for all four wheels
    """
    wear_out = 1 if tires_changed else 0.95
    return {
        "fr": {
            "incoming": {
                "wear": 0.95,
                "flat": False,
                "detached": False,
                "compound": "Medium"
            },
            "outgoing": {
                "wear": wear_out,
                "flat": False,
                "detached": False,
                "compound": "Medium"
            }
        },
        "fl": {
            "incoming": {
                "wear": 0.97,
                "flat": False,
                "detached": False,
                "compound": "Medium"
            },
            "outgoing": {
                "wear": wear_out,
                "flat": False,
                "detached": False,
                "compound": "Medium"
            }
        },
        "rl": {
            "incoming": {
                "wear": 0.94,
                "flat": False,
                "detached": False,
                "compound": "Medium"
            },
            "outgoing": {
                "wear": wear_out,
                "flat": False,
                "detached": False,
                "compound": "Medium"
            }
        },
        "rr": {
            "incoming": {
                "wear": 0.93,
                "flat": False,
                "detached": False,
                "compound": "Medium"
            },
            "outgoing": {
                "wear": wear_out,
                "flat": False,
                "detached": False,
                "compound": "Medium"
            }
        },
        "tires_changed": {
            "fl": tires_changed,
            "fr": tires_changed,
            "rl": tires_changed,
            "rr": tires_changed
        }
    }


def normalize_24h_time(time_str: str) -> str:
    """
    Normalize 24-hour time format.
    
    Converts invalid times like '24:00:00' to '00:00:00' since
    Python's datetime doesn't support hour=24.
    
    Args:
        time_str: Time string in HH:MM:SS format
        
    Returns:
        Normalized HH:MM:SS string with hour < 24
    """
    if time_str.startswith("24:"):
        return "00:" + time_str[3:]
    return time_str


def calculate_stint_time(start_time: str, end_time: str) -> timedelta:
    """
    Calculate duration between two times, accounting for day rollover.
    
    Args:
        start_time: Start time in HH:MM:SS format
        end_time: End time in HH:MM:SS format
        
    Returns:
        timedelta representing the duration
    """
    t1 = datetime.strptime(normalize_24h_time(start_time), "%H:%M:%S").time()
    t2 = datetime.strptime(end_time, "%H:%M:%S").time()
    
    dt1 = datetime.combine(date.today(), t1)
    dt2 = datetime.combine(date.today(), t2)
    
    # If start time is earlier, it must be the next day
    if dt1 < dt2:
        dt1 += timedelta(days=1)
    
    return dt1 - dt2


def calculate_time_of_day(prev_time_of_day, prev_stint_time: timedelta) -> str:
    """
    Subtract a stint duration from a given time-of-day value.
    
    This helper is used when iterating through completed stints in order to
    determine when each stint began. The algorithm simply takes the previous
    time-of-day marker (which may be a string in ``HH:MM:SS`` format or a
    :class:`datetime.time`/``datetime``) and subtracts the supplied
    ``timedelta``. The result is returned as a normalized string suitable for
    display or further arithmetic.
    
    Args:
        prev_time_of_day: Previous time-of-day value. When supplied as a string
            it must follow the ``HH:MM:SS`` format.
        prev_stint_time: Duration of the preceding stint as a :class:`timedelta`.
    
    Returns:
        A ``HH:MM:SS`` time string representing ``prev_time_of_day`` minus the
        duration. If the subtraction crosses into the previous calendar day the
        resulting time will wrap appropriately (e.g. ``00:10:00`` -
        ``00:20:00`` → ``23:50:00``).
    """
    # coerce string input to a time object
    if isinstance(prev_time_of_day, str):
        prev_time_of_day = datetime.strptime(prev_time_of_day, "%H:%M:%S").time()
    
    # if a bare datetime was given, use it directly; otherwise combine with
    # today's date to perform arithmetic.
    if isinstance(prev_time_of_day, datetime):
        dt = prev_time_of_day
    else:
        dt = datetime.combine(date.today(), prev_time_of_day)

    new_dt = dt + prev_stint_time
    return new_dt.time().strftime("%H:%M:%S")


def format_timedelta(td: timedelta) -> str:
    """
    Format timedelta as HH:MM:SS string.
    
    Args:
        td: Time duration
        
    Returns:
        Formatted string like "01:23:45"
    """
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def calc_mean_stint_time(stint_times: list[timedelta]) -> timedelta:
    """
    Calculate mean stint duration from list of timedeltas.
    
    Args:
        stint_times: List of stint durations
        
    Returns:
        Mean stint time as timedelta, or zero timedelta if list is empty
    """
    if not stint_times:
        return timedelta(0)
    
    total = sum(stint_times, timedelta(0))
    mean = total / len(stint_times)
    
    return mean


def timedelta_to_time(td: timedelta):
    """
    Convert a timedelta to a datetime.time object.
    
    Args:
        td: Time duration
        
    Returns:
        datetime.time object with hours modulo 24
    """
    
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    hours %= 24  # Wrap around if > 24
    
    return time(hour=hours, minute=minutes, second=seconds)


def is_last_stint(pit_end_time: str, mean_stint: timedelta) -> bool:
    """
    Determine whether subtracting another mean stint from the given pit time
    would roll past midnight into the previous day.

    This is used when generating pending stints; the loop should stop when
    the next subtraction would produce a time before the start of the race
    (i.e. the previous calendar day). The original implementation compared
    two ``time`` objects and only worked correctly if the pit time itself
    dipped below the mean duration, which fails when the pit time is
    represented as a simple HH:MM:SS string that wraps around past midnight.

    Args:
        pit_end_time: Current pit end time in HH:MM:SS format
        mean_stint: Mean stint duration as a :class:`timedelta`

    Returns:
        ``True`` if subtracting ``mean_stint`` would cross into the previous
        day, ``False`` otherwise.
    """
    t1 = datetime.strptime(pit_end_time, "%H:%M:%S").time()
    dt1 = datetime.combine(date.today(), t1)

    # the previous implementation accepted a ``datetime.time`` object and
    # compared two times on the same day. that logic breaks when the pit time
    # wraps past midnight, so we prefer working with a timedelta directly.
    # for backwards compatibility we still support passing a time; callers
    # should ideally supply a timedelta.
    if isinstance(mean_stint, timedelta):
        result = dt1 - mean_stint
        return result.day < dt1.day

    # ``mean_stint`` is probably a ``datetime.time`` object – fall back to
    # the original behaviour.
    dt2 = datetime.combine(date.today(), mean_stint)
    stint_time = dt1 - dt2
    return str(stint_time).startswith("-1 day")


def sanitize_stints(rows: list[list], tires: list[dict]) -> dict:
    """
    Convert table model data into database-compatible format.
    
    Args:
        rows: List of row data from table model (display format)
        tires: List of tire metadata dictionaries
        
    Returns:
        Dictionary with 'rows' and 'tires' keys containing sanitized data
    """
    sanitized_rows = []
    sanitized_tires = []

    for row in rows:
        # some consumers pass eight-element rows, others only seven; pad to
        # avoid unpack errors and ignore any extra element.
        padded = list(row) + [""]
        stint_type, name, status, pit_end_time, tires_changed, tires_left, stint_time, _ = padded[:8]

        # Convert stint_time to seconds (supports timedelta or display string)
        if isinstance(stint_time, timedelta):
            stint_time_seconds = int(stint_time.total_seconds())
        elif isinstance(stint_time, str):
            # Parse HH:MM:SS format string
            parts = [int(p) for p in stint_time.split(":")]
            while len(parts) < 3:
                parts.insert(0, 0)
            h, m, s = parts
            stint_time_seconds = h * 3600 + m * 60 + s
        else:
            stint_time_seconds = int(stint_time)
        doc = {
            "stint_type": stint_type,
            "name": name,
            "status": status == "Completed",
            "pit_end_time": _normalize_time(pit_end_time),
            "tires_changed": int(tires_changed),
            "tires_left": int(tires_left),
            "stint_time_seconds": stint_time_seconds,
        }

        sanitized_rows.append(doc)

    # propagate last valid tire set to rows without tire data
    last_tire_set = 0
    for i in range(len(rows)):
        tire = tires[i] if i < len(tires) else None
        if tire:
            sanitized_tires.append(tires[i])
            last_tire_set = i
        else:
            sanitized_tires.append(tires[last_tire_set])

    return {
        "rows": sanitized_rows,
        "tires": sanitized_tires
    }


def _normalize_time(t: str) -> str:
    """
    Normalize time string to HH:MM:SS format.
    
    Args:
        t: Time string (e.g., "1:23", "12:34:56")
        
    Returns:
        Normalized time string in HH:MM:SS format
    """
    parts = [int(p) for p in t.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts
    return f"{h:02d}:{m:02d}:{s:02d}"
