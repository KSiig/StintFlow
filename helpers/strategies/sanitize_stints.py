from datetime import timedelta

def sanitize_stints(rows):
    sanitized = []

    for row in rows:
        name, driven, pit_end_time, tires_changed, tires_left, stint_time = row

        doc = {
            "name": name,
            "driven": driven == "✅",
            "pit_end_time": normalize_time(pit_end_time),
            "tires_changed": int(tires_changed),
            "tires_left": int(tires_left),
            "stint_time_seconds": int(stint_time.total_seconds()) if isinstance(stint_time, timedelta) else int(stint_time),
        }

        sanitized.append(doc)

    return sanitized

def normalize_time(t: str) -> str:
    parts = [int(p) for p in t.split(":")]
    while len(parts) < 3:
        parts.insert(0, 0)
    h, m, s = parts
    return f"{h:02d}:{m:02d}:{s:02d}"
