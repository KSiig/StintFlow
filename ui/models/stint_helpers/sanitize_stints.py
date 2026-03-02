"""Convert table model data into database-compatible format."""

from datetime import timedelta

from ._normalize_time import _normalize_time


def sanitize_stints(rows: list[list], tires: list[dict]) -> dict:
    """Return sanitized rows/tires dict for persistence."""
    sanitized_rows = []
    sanitized_tires = []

    for row in rows:
        padded = list(row) + [""]
        stint_type, name, status, pit_end_time, tires_changed, tires_left, stint_time, time_of_day, _ = padded[:9]

        if isinstance(stint_time, timedelta):
            stint_time_seconds = int(stint_time.total_seconds())
        elif isinstance(stint_time, str):
            parts = [int(p) for p in stint_time.split(":")]
            while len(parts) < 3:
                parts.insert(0, 0)
            h, m, s = parts
            stint_time_seconds = h * 3600 + m * 60 + s
        else:
            stint_time_seconds = int(stint_time)

        tod_norm = _normalize_time(time_of_day)
        h, m, s = [int(p) for p in tod_norm.split(":")]
        tod_seconds = h * 3600 + m * 60 + s

        sanitized_rows.append(
            {
                "stint_type": stint_type,
                "name": name,
                "status": status == "Completed",
                "pit_end_time": _normalize_time(pit_end_time),
                "tires_changed": int(tires_changed),
                "tires_left": int(tires_left),
                "stint_time_seconds": stint_time_seconds,
                "time_of_day_seconds": tod_seconds,
            }
        )

    last_tire_set = 0
    for i in range(len(rows)):
        tire = tires[i] if i < len(tires) else None
        if tire:
            sanitized_tires.append(tires[i])
            last_tire_set = i
        else:
            sanitized_tires.append(tires[last_tire_set])

    return {"rows": sanitized_rows, "tires": sanitized_tires}
