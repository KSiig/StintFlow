"""Construct a default tire data dictionary."""


def get_default_tire_dict(tires_changed: bool) -> dict:
    """Return default tire data, marking changes when requested."""
    wear_out = 1 if tires_changed else 0.95
    return {
        "fr": {
            "incoming": {"wear": 0.95, "flat": False, "detached": False, "compound": "Medium"},
            "outgoing": {"wear": wear_out, "flat": False, "detached": False, "compound": "Medium"},
        },
        "fl": {
            "incoming": {"wear": 0.97, "flat": False, "detached": False, "compound": "Medium"},
            "outgoing": {"wear": wear_out, "flat": False, "detached": False, "compound": "Medium"},
        },
        "rl": {
            "incoming": {"wear": 0.94, "flat": False, "detached": False, "compound": "Medium"},
            "outgoing": {"wear": wear_out, "flat": False, "detached": False, "compound": "Medium"},
        },
        "rr": {
            "incoming": {"wear": 0.93, "flat": False, "detached": False, "compound": "Medium"},
            "outgoing": {"wear": wear_out, "flat": False, "detached": False, "compound": "Medium"},
        },
        "tires_changed": {"fl": tires_changed, "fr": tires_changed, "rl": tires_changed, "rr": tires_changed},
    }
