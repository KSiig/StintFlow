from datetime import timedelta
import json

def sanitize_stints(rows, tires):
    sanitized_rows = []
    sanitized_tires = []

    for row in rows:
        stint_type, name, status, pit_end_time, tires_changed, tires_left, stint_time = row

        doc = {
            "stint_type": stint_type,
            "name": name,
            "status": status == "Completed ✅",
            "pit_end_time": normalize_time(pit_end_time),
            "tires_changed": int(tires_changed),
            "tires_left": int(tires_left),
            "stint_time_seconds": int(stint_time.total_seconds()) if isinstance(stint_time, timedelta) else int(stint_time),
        }

        sanitized_rows.append(doc)

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

def normalize_time(t: str) -> str:
    parts = [int(p) for p in t.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts
    return f"{h:02d}:{m:02d}:{s:02d}"
