"""
Helper functions for stint table calculations.

Utility functions for converting stint types, calculating stint lengths,
and managing tire data.
"""

from datetime import datetime, date, timedelta


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
    return {
        "fr": {
            "incoming": {
                "wear": 0.95,
                "flat": False,
                "detached": False,
                "compound": "Medium"
            },
            "outgoing": {
                "wear": 1,
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
                "wear": 1,
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
                "wear": 1,
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
                "wear": 1,
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
    from datetime import time
    
    total_seconds = int(td.total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    hours %= 24  # Wrap around if > 24
    
    return time(hour=hours, minute=minutes, second=seconds)


def is_last_stint(pit_end_time: str, mean_stint_time) -> bool:
    """
    Check if subtracting mean stint time would go into negative (race finished).
    
    Args:
        pit_end_time: Current pit end time in HH:MM:SS format
        mean_stint_time: datetime.time representing mean stint duration
        
    Returns:
        True if race is finished (would go negative), False otherwise
    """
    t1 = datetime.strptime(pit_end_time, "%H:%M:%S").time()
    t2 = mean_stint_time
    
    dt1 = datetime.combine(date.today(), t1)
    dt2 = datetime.combine(date.today(), t2)
    stint_time = dt1 - dt2
    
    # If it starts with "-1 day", we've gone into negative time
    return str(stint_time).startswith("-1 day")
