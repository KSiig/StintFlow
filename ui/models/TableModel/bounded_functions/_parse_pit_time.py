from datetime import datetime


def _parse_pit_time(self, stint: dict) -> datetime:
    """Parse a stint pit end time into a sortable datetime value."""
    pit_time_str = stint.get("pit_end_time", "00:00:00")
    pit_time = datetime.strptime(pit_time_str, "%H:%M:%S").time()
    return datetime.combine(datetime.min, pit_time)
